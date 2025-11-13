from django.urls import path
from .views import (
    product_list,
    product_detail,
    product_add,
    product_edit,
    product_delete,
)

app_name = "products"

urlpatterns = [
    path("", product_list, name="product_list"),
    path("add/", product_add, name="product_add"),
    path("<int:pk>/", product_detail, name="product_detail"),
    path("<int:pk>/edit/", product_edit, name="product_edit"),
    path("<int:pk>/delete/", product_delete, name="product_delete"),
]
