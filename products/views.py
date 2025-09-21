# products/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm


# แสดงสินค้าทั้งหมด หรือกรองตามหมวดหมู่
@login_required
def product_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')

    if category_id and category_id != 'all':
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'categories': categories,
        'products': products,
        'category_id': category_id,  # ✅ ส่งกลับไปให้ template ใช้เช็ค active pill
    })


# แสดงรายละเอียดสินค้า
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


# เพิ่มสินค้าใหม่
@login_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.seller = request.user
            p.save()
            messages.success(request, 'เพิ่มสินค้าสำเร็จ ✅')
            return redirect('products:product_list')  # ✅ ใช้ namespace
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'เพิ่มสินค้า'})


# แก้ไขสินค้า (เฉพาะของตัวเอง)
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'แก้ไขสินค้าสำเร็จ ✅')
            return redirect('products:product_list')  # ✅ ใช้ namespace
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'แก้ไขสินค้า'})


# ลบสินค้า (เฉพาะของตัวเอง)
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'ลบสินค้าสำเร็จ ')
        return redirect('products:product_list')  # ✅ ใช้ namespace
    return render(request, 'products/product_confirm_delete.html', {'product': product})
