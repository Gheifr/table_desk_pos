from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic

from ordering.models import Order


@login_required
def index(request: HttpRequest):
    return render(request, "ordering/index.html", {"orders": Order.objects.all()})


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order