from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

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

        # обираємо активне меню з ?menu=ID або перше по списку
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
