from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    list_display = ModelAdmin.list_display + ("is_active", )

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ModelAdmin.list_display + ("menu_section", "price", "is_active", )
    list_filter = ("name",)
    search_fields = ("name", "menu_section", )