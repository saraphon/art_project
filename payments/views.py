import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == "paid":
        return redirect("orders:order_detail", order.id)

    items = OrderItem.objects.filter(order=order)
    if not items.exists():
        return redirect("orders:order_detail", order.id)

    line_items = [{
        "price_data": {
            "currency": "thb",
            "product_data": {"name": it.product.name},
            "unit_amount": int(it.price * 100),
        },
        "quantity": it.quantity,
    } for it in items]

    success_url = f"{settings.SITE_URL}/payments/success/?order_id={order.id}"
    cancel_url  = f"{settings.SITE_URL}/payments/cancel/?order_id={order.id}"

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=line_items,
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"order_id": str(order.id), "user_id": str(request.user.id)},
    )

    order.stripe_session_id = session.id
    order.save(update_fields=["stripe_session_id"])

    return redirect(session.url)

@login_required
def success(request):
    order_id = request.GET.get("order_id")
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != "paid" and order.stripe_session_id:
        try:
            session = stripe.checkout.Session.retrieve(order.stripe_session_id)
            if session.payment_status == "paid":
                order.status = "paid"
                order.stripe_payment_intent = session.get("payment_intent")
                order.save(update_fields=["status", "stripe_payment_intent"])
        except Exception:
            pass

    return render(request, "payments/success.html", {"order": order})

@login_required
def cancel(request):
    order_id = request.GET.get("order_id")
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "payments/cancel.html", {"order": order})

@csrf_exempt
@require_POST
def webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    if not sig_header:
        return HttpResponseBadRequest("Missing signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"].get("order_id")
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                order.status = "paid"
                order.stripe_session_id = session.get("id")
                order.stripe_payment_intent = session.get("payment_intent")
                order.save(update_fields=["status", "stripe_session_id", "stripe_payment_intent"])
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)
