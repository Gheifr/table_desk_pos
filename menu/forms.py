from django import forms

from menu.models import MenuItem, Menu


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-inline-dark"}),
        label="Menu items",
    )
    menu_sections = sorted(set(mi.menu_section.title() for mi in MenuItem.objects.filter(is_active=True)))


    class Meta:
        model = Menu
        fields = ("name", "is_active", "properties", "items")
        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-inline-dark"}),
            "properties": forms.CheckboxSelectMultiple(attrs={"class": "form-check-inline-dark"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["items"].initial = self.instance.items.all()

    def save(self, commit=True):
        menu = super().save(commit=commit)

        def save_m2m():
            menu.items.set(self.cleaned_data["items"])

        if commit:
            save_m2m()
        else:
            self.save_m2m = save_m2m

        return menu


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ["name", "menu_section", "is_active", "price", "menus"]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-inline-dark"}),
            "menus": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-inline-dark"}),
            "price": forms.NumberInput(attrs={"min": 0, "value": 0}),
        }


class MenuItemSearchForm(forms.Form):
    search_field_menu_item = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}, ),
    )
