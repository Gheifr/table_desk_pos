from django.contrib.auth.models import AbstractUser
from django.db import models

from point_of_sale.models import Property


class Employee(AbstractUser):
    position = models.CharField(max_length=50, blank=True)

    properties = models.ManyToManyField(
        Property,
        blank=True,
        related_name="employees",
    )
