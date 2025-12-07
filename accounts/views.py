from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic

from accounts.models import Employee


def index(request: HttpRequest):
    return render(request, "account/index.html")


class StaffDetailsView(generic.DetailView):
    model = Employee
    queryset = Employee.objects.filter(is_active=True).prefetch_related("tables")
    template_name = "account/staff_detail.html"