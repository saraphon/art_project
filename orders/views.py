from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Order, OrderItem

@login_required
def order_history(request):
    # โชว์เฉพาะออเดอร์ของผู้ใช้ปัจจุบัน เรียงล่าสุดก่อน
    orders_qs = Order.objects.filter(user=request.user).order_by('-id')

    # ใส่ pagination (หน้า 1 = 10 รายการ)
    paginator = Paginator(orders_qs, 10)
    page_number = request.GET.get('page') or 1
    orders_page = paginator.get_page(page_number)

    context = {
        'orders_page': orders_page,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail(request, order_id):
    # ป้องกันคนอื่นเปิดดูออเดอร์ที่ไม่ใช่ของตัวเอง
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order)

    # รวมยอด (กันเคสที่ total_price ยังไม่อัปเดต)
    computed_total = sum(i.price * i.quantity for i in items)
    total = order.total_price or computed_total

    context = {
        'order': order,
        'items': items,
        'total': total,
    }
    return render(request, 'orders/order_detail.html', context)
