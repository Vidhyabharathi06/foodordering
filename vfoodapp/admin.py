from django.contrib import admin
from vfoodapp.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','pdetails','price','is_active','pimage']

admin.site.register(Product,ProductAdmin)