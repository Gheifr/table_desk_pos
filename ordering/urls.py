from django.urls import path

from ordering import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/toggle-assignment/", views.toggle_assignment, name="toggle-assignment"),
    path("<int:pk>/edit-order/", views.order_update, name="order-edit"),
    path("create-order/", views.order_create, name="order-create"),
    path("<int:pk>/delete-order/", views.OrderDeleteView.as_view(), name="order-delete"),
    path("<int:order_pk>/edit-order/items/<int:item_pk>/remove/", views.order_item_remove, name="item-remove"),
    path("<int:pk>/items/add/", views.order_add_item, name="item-add"),
]

app_name = "orders"
