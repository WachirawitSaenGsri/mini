#model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    # โมเดลพื้นฐานสำหรับเก็บเวลาสร้างและแก้ไข
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    stock = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        (1, 'Cash'),
        (2, 'Credit Card'),
        (3, 'Debit Card'),
        (4, 'Mobile Payment'),
    ]
    id = models.BigAutoField(primary_key=True)  # หากไม่ได้กำหนด ควรใช้ `BigAutoField` ในกรณีนี้
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order {self.id} by {self.customer.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

class Member(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name_plural = 'สมาชิก'
        verbose_name = 'สมาชิก'
