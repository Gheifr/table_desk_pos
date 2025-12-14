from django.urls import path

from menu import views
from menu.views import MenuIndexView, MenuItemListView

urlpatterns = [
    path("", MenuIndexView.as_view(), name="index"),
    path("menu-items/", MenuItemListView.as_view(), name="item-index"),
    path("menu-items/create/", views.menu_item_create, name="item-create"),
    path("menu-items/<int:pk>", views.menu_item_details, name="item-detail"),
    path("menu-items/update-item/<int:pk>", views.menu_item_update, name="item-update"),
]

app_name = "menus"
