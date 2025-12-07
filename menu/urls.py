from django.urls import path

from menu.views import MenuIndexView

urlpatterns = [
    path("", MenuIndexView.as_view(), name="index"),
]

app_name = "menus"