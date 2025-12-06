from django.urls import path

from point_of_sale.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "point_of_sale"