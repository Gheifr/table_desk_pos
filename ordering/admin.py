from django.contrib import admin

from .models import OrderItem, Order


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ("menu_item__name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ("order_number",)