from django.urls import path
from . import views
from .views import (
    home, profile_view, edit_profile,
    address_list, address_add, address_edit, address_delete,
    change_email, change_phone, change_password,
    wishlist,
)

app_name = "accounts"

urlpatterns = [
    path("", home, name="home"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),

    # ที่อยู่
    path("addresses/", address_list, name="address_list"),
    path("addresses/add/", address_add, name="address_add"),
    path("addresses/edit/<int:pk>/", address_edit, name="address_edit"),
    path("addresses/delete/<int:pk>/", address_delete, name="address_delete"),

    # การตั้งค่าบัญชีของคุณเอง (ถ้าทำไว้)
    path("change-email/", change_email, name="change_email"),
    path("change-phone/", change_phone, name="change_phone"),
    path("change-password/", change_password, name="change_password"),

    path("wishlist/", wishlist, name="wishlist"),
]
