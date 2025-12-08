from decimal import Decimal

from django.db import models
from django.db.models import Max, Sum, F
from django.urls import reverse
from django.utils import timezone

from menu.models import MenuItem
from point_of_sale.models import Table


class Order(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    order_number = models.PositiveIntegerField(
        unique=True,
        editable=False,
        null=True,
        blank=True,
    )
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    guests_count = models.PositiveSmallIntegerField(default=1)

    def get_absolute_url(self):
        return reverse("orders:order-detail", args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.order_number is None:
            last_number = Order.objects.aggregate(
                Max("order_number")
            )["order_number__max"] or 0
            self.order_number = last_number + 1
        super().save(*args, **kwargs)

    def close(self):
        if not self.is_closed:
            self.is_closed = True
            self.closed_at = timezone.now()
            self.save()

    def __str__(self):
        return f"Order No: {self.order_number}, opened at: {self.opened_at}"

    @property
    def total_amount(self) -> Decimal:
        result = (
            self.order_items
            .filter(is_active=True)
            .aggregate(
                total=Sum(
                    F("quantity") * F("menu_item__price")
                )
            )["total"]
        )
        return result or Decimal("0.00")


class OrderItem(models.Model):
    is_active = models.BooleanField(default=True)

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order Item id: {self.id}, {self.menu_item.name}"
