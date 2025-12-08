from django.urls import path

from ordering import views
from ordering.views import index, OrderDetailView,  OrderDeleteView # OrderEditView,

urlpatterns = [
    path("", index, name="index"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    # path("edit-order/<int:pk>/", OrderEditView.as_view(), name="order-edit"),
    path("edit-order/<int:pk>/", views.order_update, name="order-edit"),
    path("delete-order/<int:pk>/", OrderDeleteView.as_view(), name="order-delete"),
]

app_name = "orders"