from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    categ=((1,"Pure Veg"),(2, "Non Veg"), (3,"Others"))
    name=models.CharField(max_length=50)
    price=models.FloatField()
    pdetails=models.CharField(max_length=100)
    cat=models.IntegerField(choices=categ)
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image')

class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="UserID")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="ProductID")
    qty=models.IntegerField(default=1)

class order(models.Model):
    orderId=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="UserID")
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column="ProductID")
    qty=models.IntegerField(default=1)
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    category = models.CharField(max_length=100)  # Example: Drinks, Main Course, Desserts, etc.

    def __str__(self):
        return self.name

