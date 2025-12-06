from django.db import models
from django.db.models import Max
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

    items = models.ManyToManyField(
        MenuItem,
        through="OrderItem",
        related_name="orders",
        blank=True,
    )

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
