from django.db import models

from point_of_sale.models import Property


class Menu(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    properties = models.ManyToManyField(
        "point_of_sale.Property",
        related_name="menus",
        blank=True,
    )

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    menu_section = models.CharField(max_length=50)  # 'meat', 'fish', 'kids', etc.
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    menus = models.ManyToManyField(
        Menu,
        related_name="items",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
