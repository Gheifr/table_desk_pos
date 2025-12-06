from django.urls import path

from ordering.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "orders"