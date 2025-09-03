# products/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required   # ใช้เพื่อบังคับว่าต้อง login ก่อนถึงจะเข้า view ได้
from django.contrib import messages                        # ใช้แสดงข้อความแจ้งเตือน (success, error)
from .models import Product, Category                      # import Model ที่สร้างไว้
from .forms import ProductForm                             # import Form ที่ใช้เพิ่ม/แก้ไขข้อมูลสินค้า

# ------------------------------
# แสดงสินค้าทั้งหมด หรือกรองตามหมวดหมู่
# ------------------------------
@login_required
def product_list(request):
    categories = Category.objects.all()           # ดึงหมวดหมู่ทั้งหมดจากฐานข้อมูล
    category_id = request.GET.get('category')     # เช็คว่า user กดเลือกหมวดหมู่ไหน
    if category_id:                               # ถ้ามีการเลือก category
        products = Product.objects.filter(category_id=category_id)  # กรองสินค้าเฉพาะ category นั้น
    else:
        products = Product.objects.all()          # ถ้าไม่เลือก แสดงสินค้าทั้งหมด
    return render(request, 'products/product_list.html', {
        'categories': categories,
        'products': products
    })

# ------------------------------
# แสดงรายละเอียดของสินค้าตาม id (pk = primary key)
# ------------------------------
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)   # ดึงสินค้าจากฐานข้อมูล ถ้าไม่เจอจะ error 404
    return render(request, 'products/product_detail.html', {'product': product})

# ------------------------------
# เพิ่มสินค้าใหม่
# ------------------------------
@login_required
def product_add(request):
    if request.method == 'POST':                          # ถ้าผู้ใช้กดปุ่มบันทึก
        form = ProductForm(request.POST, request.FILES)   # รับข้อมูลจากฟอร์ม (รองรับไฟล์รูปด้วย)
        if form.is_valid():                               # เช็คว่าข้อมูลฟอร์มถูกต้อง
            p = form.save(commit=False)                   # ยังไม่บันทึกลง DB ทันที
            p.seller = request.user                       # กำหนดว่าใครเป็นคนเพิ่มสินค้า
            p.save()                                      # เซฟลง DB
            messages.success(request, 'เพิ่มสินค้าสำเร็จ ✅')
            return redirect('product_list')               # กลับไปหน้ารายการสินค้า
    else:
        form = ProductForm()                              # ถ้าเพิ่งเข้ามายังไม่กด submit ให้แสดงฟอร์มเปล่า
    return render(request, 'products/product_form.html', {'form': form, 'title': 'เพิ่มสินค้า'})

# ------------------------------
# แก้ไขสินค้า (เฉพาะสินค้าที่ user คนนั้นเป็นเจ้าของเท่านั้น)
# ------------------------------
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)   # ดึงสินค้าเฉพาะที่ user คนนั้นเพิ่มไว้
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # ใส่ instance เพื่อแก้ไขสินค้าเดิม
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขสินค้าสำเร็จ ✅')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)   # ถ้ายังไม่กด submit ให้แสดงฟอร์มพร้อมข้อมูลเดิม
    return render(request, 'products/product_form.html', {'form': form, 'title': 'แก้ไขสินค้า'})

# ------------------------------
# ลบสินค้า (เฉพาะของ user ที่เป็นเจ้าของ)
# ------------------------------
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)  # ดึงสินค้าที่ user คนนั้นเป็นเจ้าของ
    if request.method == 'POST':     # ถ้ากดยืนยันการลบ
        product.delete()             # ลบสินค้าออกจาก DB
        messages.success(request, 'ลบสินค้าสำเร็จ 🗑️')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})
