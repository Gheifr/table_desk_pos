from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic

from accounts.models import Employee


@login_required
def index(request: HttpRequest):
    return render(request, "account/index.html")


class StaffDetailsView(LoginRequiredMixin, generic.DetailView):
    model = Employee
    queryset = Employee.objects.filter(is_active=True).prefetch_related("tables")
    template_name = "account/staff_detail.html"
