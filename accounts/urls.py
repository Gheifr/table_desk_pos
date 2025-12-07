from django.urls import path

from accounts.views import index, StaffDetailsView

urlpatterns = [
    path("", index, name="index"),
    path("<int:pk>/", StaffDetailsView.as_view(), name="staff-detail"),
]

app_name = "accounts"
