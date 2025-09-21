from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("create-checkout-session/<int:order_id>/", views.create_checkout_session, name="create_checkout_session"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path("webhook/", views.webhook, name="webhook"),
]
