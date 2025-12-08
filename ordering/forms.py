from django import forms
from django.forms import inlineformset_factory

from point_of_sale.models import Table
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table", "is_closed", "closed_at", "guests_count"]
        widgets = {
            "table": forms.Select(attrs={
                "class": "form-select form-select-sm bg-white text-dark m-0",
            }),
            "closed_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            # "order_items": forms.CheckboxSelectMultiple(),
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["menu_item", "quantity", "is_active"]


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)
