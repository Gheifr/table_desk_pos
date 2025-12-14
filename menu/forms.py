from django import forms

from menu.models import MenuItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "menu_section", "is_active", "price", "menus"]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-inline-dark"}),
            "menus": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-inline-dark"}),
            "price": forms.NumberInput(),
        }

class MenuItemSearchForm(forms.Form):
    search_field_menu_item = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )