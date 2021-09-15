from django.contrib import admin
from .models import Category, Product, Cart, CartItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name', )}
    list_display = ('product_name', 'category', 'quantity', 'price', 'is_stock', 'created_at')
    list_filter = ('product_name', 'category', 'price', 'is_stock')

admin.site.register(Product, ProductAdmin)  
admin.site.register(Cart)    
admin.site.register(CartItem)    

