from django.urls import path

from menu import views

urlpatterns = [
    path("", views.MenuIndexView.as_view(), name="index"),
    path("create/", views.menu_create, name="menu-create"),
    path("update/<int:pk>", views.menu_update, name="menu-update"),
    path("delete/<int:pk>", views.menu_delete, name="menu-delete"),
    path("menu-items/", views.MenuItemListView.as_view(), name="item-index"),
    path("menu-items/create/", views.menu_item_create, name="item-create"),
    path("menu-items/<int:pk>", views.menu_item_details, name="item-detail"),
    path("menu-items/update-item/<int:pk>", views.menu_item_update, name="item-update"),
    path("menu-items/delete-item/<int:pk>", views.menu_item_try_delete, name="item-delete"),
    path("menu-items/confirm-delete-item/<int:pk>", views.menu_item_confirm_delete, name="item-confirm-delete-in-menu"),
]

app_name = "menus"
