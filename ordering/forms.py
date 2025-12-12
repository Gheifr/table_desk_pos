from django import forms
from django.db.models import fields

from accounts.models import Employee
from point_of_sale.models import Table
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


class OrderCreateForm(forms.ModelForm):
    # hidden field in order to avoid
    # browser attempts to resend data when there were
    # form errors and user cancels order creation
    is_cancelled = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Order
        fields = ["table", "guests_count"]
        widgets = {
            "table": forms.Select(attrs={
                "class": "form-select form-select-sm bg-white w-auto text-dark m-0",
            }),
            "guests_count": forms.NumberInput(
                attrs={"type": "number", "class": "form-control form-control-sm w-auto", "min": 1}),
            "total_amount": forms.TextInput(attrs={"type": "number", "class": "form-control form-control-sm"}),
        }


    def clean_table(self):
        table = self.cleaned_data.get("table")
        if table is None:
            raise forms.ValidationError("Please select a table.")
        return table