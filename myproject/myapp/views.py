# Create your views here.
# views.py
from django.shortcuts import render, redirect
from myapp.models import Product, Order, OrderItem, Customer
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from myapp.forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def home_view(request):
    return render(request,'base.html')


@login_required
def order_summary(request):
    orders = Order.objects.select_related('customer').prefetch_related('items__product').all()
    context = {'orders': orders}
    return render(request, 'base.html', context)

@login_required
def create_order(request):
    products = Product.objects.all()
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        product_name = request.POST.get('product')
        quantity = request.POST.get('quantity')
        payment_method = int(request.POST.get('payment_method'))  # เปลี่ยนเป็น int

        # ตรวจสอบว่ามี Customer ที่มี email ซ้ำหรือไม่
        existing_customer = Customer.objects.filter(email=customer_email).first()
        if existing_customer:
            messages.error(request, f"Customer with email {customer_email} already exists.")
            return render(request, 'create_order.html', {'products': products})

        # หากไม่มีลูกค้าที่ซ้ำกัน ให้สร้างลูกค้าใหม่
        customer = Customer.objects.create(name=customer_name, email=customer_email)

        # Find the product by name
        product = Product.objects.filter(name=product_name).first()
        if not product:
            messages.error(request, "Product not found. Please check the product name.")
            return render(request, 'create_order.html', {'products': products})

        # Calculate total price
        total_price = product.price * int(quantity)

        # Create the order (อ้างอิง customer ที่บันทึกแล้ว)
        order = Order.objects.create(
            customer=customer,
            total_price=total_price,
            payment_method=payment_method
        )

        # Create the OrderItem
        OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)

        messages.success(request, "Order created successfully!")
        return redirect('order_success', order_id=order.id)

    return render(request, 'create_order.html', {'products': products})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    products = Product.objects.all()

    if request.method == 'POST':
        # Update the customer details
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        order.customer.name = customer_name
        order.customer.email = customer_email
        order.customer.save()

        # Update the order item details
        product_name = request.POST.get('product')
        quantity = request.POST.get('quantity')
        payment_method = int(request.POST.get('payment_method'))

        product = Product.objects.filter(name=product_name).first()
        if not product:
            messages.error(request, "Product not found. Please check the product name.")
            return render(request, 'edit_order.html', {'order': order, 'products': products})

        # Update Order Item
        order_item = order.items.first()  # Assuming each order has only one item
        order_item.product = product
        order_item.quantity = quantity
        order_item.price = product.price
        order_item.save()

        # Update Order Details
        order.total_price = product.price * int(quantity)
        order.payment_method = payment_method
        order.save()

        messages.success(request, "Order updated successfully!")
        return redirect('order_list')

    context = {'order': order, 'products': products}
    return render(request, 'edit_order.html', context)

# Delete Order View
@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted successfully!")
        return redirect('order_list')

    context = {'order': order}
    return render(request, 'delete_order.html', context)

@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order_id': order_id})
@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})
@login_required
def shop_view(request):
    orders = Order.objects.all()
    return render(request, 'base.html', {'orders': orders})


'''def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # บันทึกผู้ใช้ลงในฐานข้อมูล
            login(request, user)  # ล็อกอินผู้ใช้หลังจากลงทะเบียน
            return redirect('home')  # เปลี่ยนเป็นหน้าที่คุณต้องการให้ redirect ไปหลังจากสมัครเสร็จ
    else:
        form = UserRegisterForm()
    return render(request, 'member_register_form_decor.html', {'form': form})'''
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # บันทึกผู้ใช้ลงในฐานข้อมูล
            login(request, user)  # ล็อกอินผู้ใช้หลังจากลงทะเบียน
            messages.success(request, "Registration successful!")  # ข้อความแจ้งเตือนเมื่อสมัครสมาชิกสำเร็จ
            return redirect('login')  # เปลี่ยนไปหน้าหลักหลังจากสมัครสำเร็จ
        else:
            messages.error(request, "Registration failed. Please check the information and try again.")  # ข้อความเมื่อมีข้อผิดพลาดในการสมัคร
    else:
        form = UserRegisterForm()
    return render(request, 'member_register_form_decor.html', {'form': form})