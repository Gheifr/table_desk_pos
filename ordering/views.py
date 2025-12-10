from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum, QuerySet
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic

from menu.models import MenuItem
from ordering.forms import OrderForm, OrderItemCreateForm
from ordering.models import Order, OrderItem


@login_required
def index(request: HttpRequest):
    return render(request, "ordering/index.html",
                  {"orders": Order.objects.prefetch_related("employees").select_related("table").all()})


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    queryset = Order.objects.prefetch_related("employees").select_related("table")


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    pass


def combine_items(order):
    grouped = (
        order.order_items
        .values("menu_item")
        .annotate(total_qty=Sum("quantity"))
    )

    for row in grouped:
        menu_item_id = row["menu_item"]
        total_qty = row["total_qty"]

        items = list(
            order.order_items
            .filter(menu_item_id=menu_item_id)
            .order_by("id")
        )
        if not items:
            continue

        first, *rest = items

        if first.quantity != total_qty:
            first.quantity = total_qty
            first.save()

        if rest:
            order.order_items.filter(id__in=[oi.id for oi in rest]).delete()


@login_required
def order_update(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("table").prefetch_related("order_items__menu_item").prefetch_related("employees"),
        pk=pk,
    )

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            with transaction.atomic():
                form.save()

                for order_item in order.order_items.all():
                    field_name = f"qty_{order_item.id}"
                    raw_value = request.POST.get(field_name)
                    if raw_value is None:
                        continue
                    try:
                        qty = int(raw_value)
                    except ValueError:
                        continue

                    if qty > 0:
                        order_item.quantity = qty
                        order_item.save()
                    else:
                        order_item.delete()

                if order.order_items:
                    combine_items(order)

            return redirect("orders:order-detail", pk=order.pk)
    else:
        form = OrderForm(instance=order)

    return render(
        request,
        "ordering/order_form.html",
        {
            "order": order,
            "form": form,
            "add_item_form": OrderItemCreateForm(),
        },
    )


@login_required
def order_item_remove(request, order_pk, item_pk):
    order = get_object_or_404(Order, pk=order_pk)
    order_item = get_object_or_404(OrderItem, pk=item_pk, order=order)

    if request.method == "POST":
        order_item.delete()

    return redirect("orders:order-edit", pk=order.pk)


@login_required
def order_add_item(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        form = OrderItemCreateForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()

    return redirect("orders:order-edit", pk=order.pk)


@login_required
def toggle_assignment(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user in order.employees.all():
        order.employees.remove(request.user)
    else:
        order.employees.add(request.user)

    return redirect("orders:order-detail", pk=order.pk)
