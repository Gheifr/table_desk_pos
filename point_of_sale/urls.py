from django.urls import path

from point_of_sale import views

urlpatterns = [
    path("", views.index, name="index"),
]

app_name = "point_of_sale"
