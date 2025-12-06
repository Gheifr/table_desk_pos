from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser):
    position = models.CharField(max_length=50, blank=True)

    properties = models.ManyToManyField(
        "point_of_sale.Property",
        blank=True,
        related_name="employees",
    )

    def __str__(self):
        full_name = self.get_full_name() or self.username
        if self.position:
            return f"{full_name} ({self.position})"
        return full_name
