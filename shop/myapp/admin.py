from django.contrib import admin

from myapp.models import Category, Brand, Product, CartItem, Cart, Order
# Register your models here.

def make_published(modeladmin, request, queryset):
	queryset.update(status="Оплачено")
make_published.short_description = "Оплачено"


class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_published]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)