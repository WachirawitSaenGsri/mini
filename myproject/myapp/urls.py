# urls
from django.urls import path
from myapp import views
from myapp import classview
from myapp.classview import *

urlpatterns = [
    path('order-summary/', views.order_summary, name='order_summary'),
    path('home/', views.home_view, name='home'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order-list/', views.order_list, name='order_list'),
    path('', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),  # เพิ่มเส้นทางสำหรับแก้ไข
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
]


