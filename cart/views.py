from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from orders.models import Order, OrderItem


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f'เพิ่ม {product.name} x{quantity} ไปยังตะกร้าแล้ว ✅')
    return redirect('cart:cart_detail')   # ✅


@login_required
def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
            messages.success(request, 'อัปเดตจำนวนสินค้าแล้ว ✅')
        else:
            item.delete()
            messages.success(request, 'ลบสินค้าออกจากตะกร้าแล้ว 🗑️')
    return redirect('cart:cart_detail')   # ✅


@login_required
def cart_update_quantity(request, item_id):
    if request.method == "POST":
        qty = int(request.POST.get("quantity", 1))
        if qty < 1:
            qty = 1

        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.quantity = qty
            item.save()
            return JsonResponse({
                "success": True,
                "new_total": item.quantity * item.product.price
            })
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False}, status=404)

    return JsonResponse({"success": False}, status=400)


@login_required
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'ลบสินค้ารายการนี้เรียบร้อยแล้ว 🗑️')
    return redirect('cart:cart_detail')   # ✅


@login_required
def cart_delete(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'ล้างตะกร้าเรียบร้อยแล้ว ')
    return redirect('cart:cart_detail')   # ✅


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total_price': total_price,
    })


@login_required
def cart_delete_selected(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        if selected_ids:
            CartItem.objects.filter(id__in=selected_ids, cart__user=request.user).delete()
            messages.success(request, "ลบสินค้าที่เลือกแล้ว ")
    return redirect('cart:cart_detail')   # ✅


@login_required
def checkout(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        items = CartItem.objects.filter(id__in=selected_ids, cart__user=request.user)

        if not items.exists():
            messages.error(request, "กรุณาเลือกสินค้าอย่างน้อย 1 รายการ")
            return redirect("cart:cart_detail")   # ✅

        full_name = request.POST.get("full_name", "N/A").strip() or "N/A"
        address = request.POST.get("address", "N/A").strip() or "N/A"
        phone = request.POST.get("phone", "N/A").strip() or "N/A"

        order = Order.objects.create(
            user=request.user,
            status="pending",
            full_name=full_name,
            address=address,
            phone=phone,
        )

        total = 0
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            total += item.product.price * item.quantity

        order.total_price = total
        order.save()

        items.delete()

        messages.success(request, f"สร้างคำสั่งซื้อ #{order.id} เรียบร้อย ✅")
        return redirect("order_history")

    return redirect("cart:cart_detail")   # ✅


@login_required
def checkout_info(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        items = CartItem.objects.filter(id__in=selected_ids, cart__user=request.user)
        if not items.exists():
            messages.error(request, "กรุณาเลือกสินค้าอย่างน้อย 1 รายการ")
            return redirect("cart:cart_detail")

        return render(request, "cart/checkout_info.html", {
            "items": items  # ส่ง CartItem objects ให้ template
        })
    return redirect("cart:cart_detail")




@login_required
def checkout_confirm(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        items = CartItem.objects.filter(id__in=selected_ids, cart__user=request.user)
        if not items.exists():
            messages.error(request, "ไม่พบสินค้า")
            return redirect("cart:cart_detail")   # ✅

        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            status="pending",
            total_price=0
        )

        total = 0
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.product.price * item.quantity

        order.total_price = total
        order.save()

        items.delete()

        messages.success(request, f"สร้างคำสั่งซื้อ #{order.id} เรียบร้อย ✅ (ชำระผ่าน {payment_method})")
        return redirect("order_history")

    return redirect("cart:cart_detail")   # ✅
