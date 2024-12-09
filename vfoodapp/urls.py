from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from vfoodapp import views

urlpatterns = [ 
        path('home',views.home),
        path('register',views.register),
        path('login',views.user_login),
        path('logout',views.user_logout),
        path('about',views.about),
        path('menu',views.menu),
        path('search/', views.search_view, name='search'),
        path('contact',views.contact),
        path('catfilter/<cv>',views.catagory),
        path('range',views.range),
        path('sort/<sv>',views.sort),
        path('pdetials/<pid>',views.pdetials),
        path('addtocart/<pid>',views.addtocart),
        path('viewcart',views.viewcart),
        path('remove/<cid>',views.remove),
        path('update/<qv>/<cid>',views.updateQty),
        path('menu/<int:id>/', views.menu_item_detail, name='menu_item_detail'),
        path('search/', views.search_view, name='search'),
        path('placeorder/', views.placeorder, name='placeorder'),  # 'placeorder' is the pattern name
        path('makepayment/', views.Makepayment, name='Makepayment'),  # The name must be 'Makepayment'

        


]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)