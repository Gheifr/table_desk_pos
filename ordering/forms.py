from django import forms

from accounts.models import Employee
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table", "guests_count", "employees"]
        widgets = {
            "table": forms.Select(attrs={
                "class": "form-select form-select-sm bg-white w-auto text-dark m-0",
            }),
            "employees": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-inline-dark",
            }),
            "guests_count": forms.NumberInput(
                attrs={"type": "number", "class": "form-control form-control-sm w-auto", "min": 1}),
            "total_amount": forms.TextInput(attrs={"type": "number", "class": "form-control form-control-sm"}),
        }


class OrderItemCreateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity"]
        widgets = {
            "menu_item": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control form-control-sm",
                "min": 1,
                "value": 1,
            }),
        }
