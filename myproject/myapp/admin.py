from django.contrib import admin
from myapp.models import *
# Register your models here.
from django.contrib import admin
from myapp.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock')
    list_editable = ('price', 'stock')
    search_fields = ('name',)
    list_filter = ('price', 'stock')

    # ใช้ fieldsets เพื่อจัดกลุ่มฟิลด์
    fieldsets = (
        (None, {
            'fields': ('name', 'price')
        }),
        ('Stock Information', {
            'fields': ('stock',),
            'description': 'รายละเอียดเกี่ยวกับจำนวนสินค้าที่เหลือ'
        }),
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)
admin.site.register(Member)


