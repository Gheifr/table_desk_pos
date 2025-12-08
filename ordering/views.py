from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from ordering.forms import OrderForm, OrderItemFormSet
from ordering.models import Order


@login_required
def index(request: HttpRequest):
    return render(request, "ordering/index.html", {"orders": Order.objects.select_related("table").all()})


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    queryset = Order.objects.select_related("table").prefetch_related("table__employees")


# class OrderEditView(LoginRequiredMixin, generic.UpdateView):
#     model = Order
#     fields = ["guests_count","table"]
#     pass


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    pass


@login_required
def order_update(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("table").prefetch_related("order_items__menu_item"),
        pk=pk,
    )

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # тут можеш одразу перераховувати total або просто редірект
            return redirect("orders:detail", pk=order.pk)
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)

    context = {
        "order": order,
        "form": form,
        "formset": formset,
    }
    return render(request, "ordering/order_form.html", context)