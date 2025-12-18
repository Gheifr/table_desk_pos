from django.urls import path

from accounts import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.StaffDetailsView.as_view(), name="staff-detail"),
]

app_name = "accounts"
