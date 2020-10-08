from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(ContactMessage)

#orders 
class OrdersItemAdmin(admin.StackedInline):
    model = OrderItem
    extra=0
class ShippingAddressAdmin(admin.StackedInline):
    model = ShippingAddress
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrdersItemAdmin, ShippingAddressAdmin]
 
    class Meta:
       model = Order
 
@admin.register(OrderItem)
class OrdersItemAdmin(admin.ModelAdmin):
    pass

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    pass

#product & image
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    extra=0
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
 
    class Meta:
       model = Product
 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass