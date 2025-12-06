from django.contrib import admin

from models import Property, Table


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    search_fields = ("table_number",
                     "employees__username",
                     "employees__first_name",
                     "employees__last_name",
                     )
