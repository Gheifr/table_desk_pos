from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render
from django.views import generic

from menu.forms import MenuItemForm, MenuItemSearchForm
from menu.models import MenuItem, Menu


class MenuIndexView(LoginRequiredMixin, generic.ListView):
    model = MenuItem
    template_name = "menu/index.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        menus = (
            Menu.objects
            .filter(is_active=True, items__isnull=False)
            .prefetch_related("items")
            .order_by("name")
            .distinct()
        )
        context["menus"] = menus

        menu_id = self.request.GET.get("menu")
        active_menu = None
        if menu_id:
            active_menu = menus.filter(pk=menu_id).first()
        if not active_menu and menus.exists():
            active_menu = menus.first()
        context["active_menu"] = active_menu

        sections = []
        items_by_section = {}

        if active_menu:
            items = (
                MenuItem.objects.filter(is_active=True, menus=active_menu)
                .order_by("menu_section", "name")
            )
            for item in items:
                sec = item.menu_section or "Other"
                if sec not in items_by_section:
                    items_by_section[sec] = []
                    sections.append(sec)
                items_by_section[sec].append(item)

        context["sections"] = sections
        context["items_by_section"] = items_by_section
        return context


@login_required
def menu_item_details(request, pk):
    return redirect("menus:item-update", pk=pk)


class MenuItemListView(LoginRequiredMixin, generic.ListView):
    model = MenuItem
    paginate_by = 10
    template_name = "menu/menuitem_list.html"

    def get_context_data(self, **kwargs):
        context = super(MenuItemListView, self).get_context_data(**kwargs)
        search_field_menu_item = self.request.GET.get(
            "search_field_menu_item",
            ""
        )
        context["search_field_menu_item"] = search_field_menu_item
        context["search_form"] = MenuItemSearchForm(
            initial={"search_field_menu_item": search_field_menu_item}
        )
        return context

    def get_queryset(self):
        queryset = MenuItem.objects.prefetch_related("menus")
        form = MenuItemSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["search_field_menu_item"]
            )
        return queryset


@login_required()
def menu_item_update(request, pk):
    menu_item = get_object_or_404(
        MenuItem.objects.prefetch_related("menus"),
        pk=pk
    )
    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=menu_item)

        if form.is_valid():
            with transaction.atomic():
                form.save()

                for menu in menu_item.menus.all():

                    mi = menu.items

                    if not menu_item in menu.items.all():
                        menu.items.add(menu_item)

        return redirect("menus:item-index")
    else:
        form = MenuItemForm(instance=menu_item)

    return render(
        request,
        "menu/menuitem_form.html",
        {
            "menu_item": menu_item,
            "form": form,
        }
    )


@login_required()
def menu_item_create(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("menus:item-index")
        else:
            return render(request, "menu/menuitem_form.html", {"form": form})

    else:
        form = MenuItemForm()
        return render(request, "menu/menuitem_form.html", {"form": form})


@login_required()
def menu_item_try_delete(request, pk):
    menu_item = get_object_or_404(MenuItem.objects.all(), pk=pk)

    if request.method == "GET":
        return render(
            request,
            'menu/menuitem_confirm_delete.html',
            {
                "menuitem": menu_item,
            }
        )
    else:
        if menu_item.menus.all().count() > 0:
            return redirect("menus:item-confirm-delete-in-menu", pk=menu_item.pk)
        else:
            menu_item.delete()
        return redirect("menus:item-index")


@login_required()
def menu_item_confirm_delete(request, pk):
    menu_item = get_object_or_404(MenuItem.objects.all(), pk=pk)

    if request.method == "GET":
        return render(request, "menu/menuitem_confirm_delete_in_menu.html", {"menuitem": menu_item})
    else:
        for menu in menu_item.menus.all():
            menu_item.menus.remove(menu)

        menu_item.delete()

    return redirect("menus:item-index")
