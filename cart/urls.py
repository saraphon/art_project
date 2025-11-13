from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("update/<int:item_id>/", views.cart_update, name="cart_update"),
    path("update_qty/<int:item_id>/", views.cart_update_quantity, name="cart_update_quantity"),
    path("remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
    path("delete/", views.cart_delete, name="cart_delete"),
    path("delete_selected/", views.cart_delete_selected, name="cart_delete_selected"),
    
    # ✅ เชื่อม Checkout flow
    path("checkout/", views.checkout_info, name="checkout_info"),
    path("checkout/confirm/", views.checkout_confirm, name="checkout_confirm"),

    
]
