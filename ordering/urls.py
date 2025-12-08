from django.urls import path

from ordering.views import index, OrderDetailView

urlpatterns = [
    path("", index, name="index"),
    path("<int:pk>", OrderDetailView.as_view(), name="order-detail"),
]

app_name = "orders"