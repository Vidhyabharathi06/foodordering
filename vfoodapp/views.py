from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from vfoodapp.models import Product,order,cart,MenuItem #===DB table
import random, razorpay
MenuItem.objects.all()

# Create your views here.
def home(request):
    context={}
    #ORM==== object relation mapping
    #onject===== retaion(table)==v=class table la maruthu
    p=Product.objects.filter(is_active=True)#id
    context['products']=p
    return render(request,'index.html',context)

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')

from django.shortcuts import render
from .models import MenuItem

# Search View
def search_view(request):
    query = request.GET.get('q')  # Get the search query from the form
    results = MenuItem.objects.none()  # Default empty queryset

    if query:
        print(f"Search Query: {query}")  # Debugging - to check the query
        # Search both 'name' and 'description' fields for matches
        results = MenuItem.objects.filter(
            name__icontains=query
        ) | MenuItem.objects.filter(description__icontains=query)
        print(f"Results: {results}")  # Debugging - to check results

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)
def menu_item_detail(request, id):
    item = get_object_or_404(MenuItem, id=id)  # Get the menu item by ID
    context = {
        'item': item,
    }
    return render(request, 'menu_item_detail.html', context)  # This will render the detail template



product = Product.objects.first()  # Or any product you want to check
print(product.pimage.url)  # This should print the image URL


def catagory(request,cv):
    #select * from product where is_active=true and cat=1 
    q1=Q(is_active=True)# it is replaceable, cat=1---> By mobiles
    q2=Q(cat=cv)
    #select * from prodect, is_active and cat_1
    p=Product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)


#To calculate min and max range:
def range(request):
  #select * from  product where price >=500 and price <=4000 and is_active=true
  #500
   minrange=request.GET['Min']
   maxrange=request.GET['Max']
   q1=Q(price__gte=minrange)#500
   q2=Q(price__lte=maxrange)#4000
   q3=Q(is_active=True)
   p=Product.objects.filter(q1 & q2 & q3)
   context={}
   context['products']=p
   return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':#ascending
        col='price'
    else:
        col='-price'#decending
    p=Product.objects.filter(is_active=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)

def pdetials(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'productdetails.html',context)
 
def addtocart(request,pid):
     #to  check whether the user is authorized user or not 
     if request.user.is_authenticated:
         userID=request.user.id
         u=User.objects.filter(id=userID)#User--- Uid, password, email
         p=Product.objects.filter(id=pid)#product--pid,name,price,description
         c=cart.objects.create(uid=u[0],pid=p[0])
         c.save()
         context={}
         context['products']=p
         #return HttpResponse('product is added to cart')
         return render(request,'productdetails.html',context)

     else:

         return redirect(request,'/login')
     
def viewcart(request):
      UserID=request.user.id
      c=cart.objects.filter(uid=UserID) 
      s=0
      count=len(c)
      for x in c:# 1, laptop, 3500,. 2, watch,2500
          #0=0+ 3500
          #3500=3500+2500
          #
          s=s+x.pid.price * x.qty
          context={}
          context['n']=count
          context['total']=s
          context['products']=c 
     
          return render(request,'cart.html',context)


def remove(request,cid):
    c=cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')


def updateQty(request, qv, cid):
    # Fetch the cart item by its ID
    c = cart.objects.filter(id=cid)

    # Ensure the cart item exists
    if c.exists():
        cart_item = c.first()  # Safely get the first item

        # If the 'qv' parameter is '1', increment the quantity
        if qv == '1':
            cal = cart_item.qty + 1
            c.update(qty=cal)

        # If 'qv' is not '1', decrement the quantity but ensure it doesn't go below 1
        else:
            if cart_item.qty > 1:
                cal = cart_item.qty - 1
                c.update(qty=cal)

    # After updating the quantity, redirect to the view cart page
    return redirect('/viewcart')

# def updateQty(request,qv,cid):
#     c=cart.objects.filter(id=cid)

#     if qv=='1':
#         cal=c[0].qty+1
#         c.update(qty=cal)
#     else:
#       if c[0].qty>1: 
#        cal=c[0].qty-1
#        c.update(qty=cal)     


    # return redirect('/viewcart')

# def placeorder(request):
#     UserID=request.user.id
#     c=cart.objects.filter(uid=UserID) 
#     #random is the predefined package to automatically generate the random numbers from the 
#     #given range,  randrange(1000,9999)
#     oid=random.randrange(1000,9999)

#     for x in c:
#         o=order.objects.create(orderId=oid,pid=x.pid,uid=x.uid,qty=x.qty)
#         o.save()
#         x.delete()

#     order1=order.objects.filter(uid=request.user.id)
#     s=0
#     count=len(order1)
#     for x in order1:
#         s=s+x.pid.price * x.qty
#         context={}
#         context['n']=count
#         context['total']=s
#         context['products']=order1
#     return render(request,'placeorder.html',context)
def placeorder(request):
    UserID = request.user.id
    c = cart.objects.filter(uid=UserID)

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        oid = random.randrange(1000, 9999)

        # Create orders for each item in the cart
        for x in c:
            o = order.objects.create(orderId=oid, pid=x.pid, uid=x.uid, qty=x.qty)
            o.save()
            x.delete()

        return redirect('Makepayment')  # Redirect to the payment view

    else:
        # Handle GET request
        order1 = order.objects.filter(uid=request.user.id)
        s = 0
        count = len(order1)
        for x in order1:
            s += x.pid.price * x.qty
        
        context = {
            'n': count,
            'total': s,
            'products': order1
        }
        return render(request,'placeorder.html', context)


def Makepayment(request):
    order1=order.objects.filter(uid=request.user.id)
    s=0
    for x in order1:
        s=s+x.pid.price * x.qty
        id=x.orderId

    client = razorpay.Client(auth=("rzp_test_VILGzeKQgbpDGz", "8ov2EtXxvPorWWZFq2XK7Wxv"))

    data = { "amount": s*100, "currency": "INR", "receipt": id }
    payment = client.order.create(data=data)
    context={}
    context['data']=payment
    order1.delete()

    return render(request,'pay.html',context)



def register(request):
    if request.method=="POST":
        #the user entered value is stored into assigned variables
        #the flieds cannot be  empty
        context={}
        #user entered value is stored into assigned variables
        userName=request.POST['uname']#vidhya
        passw=request.POST['upass']#123
        cpassword=request.POST['cpass']#123

        #checking all fields are blamk on the "register.html"
        #Error message will get printed on the "registed.html"
        if userName=="" or passw=="" or cpassword=="":
            context['errormessage']="Fields cannot be blank"
            return render(request,'register.html',context)
        
        elif passw!=cpassword:
             context['errormessage']="Passward and confirm passward must be same"
             return render(request,'register.html',context)
        else:
            try:

   
        #                    models=views
        #              auth_user/user===> username
        #                 table  --  vidhya
                u=User.objects.create(username=userName,password=passw,email=cpassword)
                #To access the password from the  table auth_user
                #it will provide the password  
                u.set_password(passw)
                u.save()
                context['success']='user created Successfully! please login'
                return render(request,'register.html',context)
            except Exception:
                 context['errormessage']='user with same name already exists!!'
                 return render(request,'register.html',context)
    return render(request,'register.html')
def user_login(request):
    if request.method=="POST":
        #the user entered value is stored into assigned variables
        #the flieds cannot be  empty
        context={}
        #user entered value is stored into assigned variables
        LoginName=request.POST['lname']#vidhya
        Loginpass=request.POST['lpass']#123

        if LoginName=="" or Loginpass=="":
            context['err']="Fields cannot be blank"
            return render(request,'login.html',context)
        else:
            #authentication --- It is the predefined method provided Django framework.
            # It is used to compare the username and password from the auth_user table.
            # That table is stored in mysql
            u=authenticate(username=LoginName,password=Loginpass) 
            print(u)
            #it is automatically used to redirect from one page to another
            if u is not None: #vidhya , 231 is not none.
                login(request,u)
                return redirect('/home')
            else:
                context['err']='invalid user'
                return render(request,'login.html',context)
    else:

        return render(request,'login.html')
       
def user_logout(request):
        logout(request)
        return redirect('/home')
