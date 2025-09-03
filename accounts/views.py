from django.shortcuts import render, redirect, get_object_or_404

from orders.models import Order
from .forms import ProfileForm, AddressForm   # ✅ เพิ่ม AddressForm
from .models import Profile, Address          # ✅ เพิ่ม Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product 

@login_required
def home(request):
    # ดึงสินค้าขายดี 3 ชิ้นแรก
    best_selling_products = Product.objects.all()[:3]
    return render(request, 'account/home.html', {
        'best_selling_products': best_selling_products
    })


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'account/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว ✅')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'account/edit_profile.html', {
        'form': form,
        'profile': profile
    })


# ✅ ---- ฟังก์ชันสำหรับจัดการที่อยู่ ----
@login_required
def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'account/address_list.html', {'addresses': addresses})

@login_required
def address_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'เพิ่มที่อยู่เรียบร้อยแล้ว ✅')
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'account/address_form.html', {'form': form})

@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'ลบที่อยู่เรียบร้อยแล้ว 🗑️')
        return redirect('address_list')
    return render(request, 'account/address_confirm_delete.html', {'address': address})

@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขที่อยู่เรียบร้อยแล้ว ✅')
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)

    return render(request, 'account/address_form.html', {'form': form})


# ✅ ---- ฟังก์ชันใหม่ ----
@login_required
def change_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            messages.success(request, 'เปลี่ยนอีเมลเรียบร้อยแล้ว ✅')
            return redirect('profile')
    return render(request, 'account/change_email.html')

@login_required
def change_phone(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        new_phone = request.POST.get('phone')
        if new_phone:
            profile.phone = new_phone
            profile.save()
            messages.success(request, 'เปลี่ยนเบอร์โทรเรียบร้อยแล้ว ✅')
            return redirect('profile')
    return render(request, 'account/change_phone.html', {'profile': profile})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'รหัสผ่านเดิมไม่ถูกต้อง ❌')
        elif new_password != confirm_password:
            messages.error(request, 'รหัสผ่านใหม่ไม่ตรงกัน ❌')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'เปลี่ยนรหัสผ่านเรียบร้อยแล้ว ✅')
            return redirect('account_login')

    return render(request, 'account/change_password.html')

@login_required
def wishlist(request):
    # ตัวอย่างดึงข้อมูล wishlist จาก DB (ต้องสร้าง Model เพิ่มเอง)
    wishlist_items = []  # ใส่ QuerySet ของสินค้าที่ถูกใจ
    return render(request, 'account/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/order_history.html", {"orders": orders})




