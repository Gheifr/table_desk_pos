from django.db import models


class Property(models.Model):
    name = models.CharField(max_length=255)
    number_tables = models.PositiveIntegerField()


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
        Employee,
        related_name="tables",
        blank=True,
    )

    class Meta:
        # unique table number per property
        constraints = [
            models.UniqueConstraint(
                fields=["property", "table_number"],
                name="unique_table_per_property",
            )
        ]
