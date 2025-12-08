from django.conf import settings
from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=255)
    number_tables = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Table(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.PROTECT,
        related_name="tables",
    )
    table_number = models.PositiveIntegerField()
    max_guests_num = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    employees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tables",
        blank=True,
    )

    def __str__(self):
        return f"Table No: {self.table_number}, {f"seats: {self.max_guests_num}"}"

    class Meta:
        ordering = ["table_number"]
        # unique table number per property
        constraints = [
            models.UniqueConstraint(
                fields=["property", "table_number"],
                name="unique_table_per_property",
            )
        ]
