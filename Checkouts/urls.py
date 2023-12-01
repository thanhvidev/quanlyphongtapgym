from django.contrib import admin
from django.urls import path, include
from . import views

# urlpatterns = [
#     path('checkout/<int:course_id>', views.Checkout, name='checkout'),
#     path('payment-success/<int:course_id>/',
#          views.PaymentSuccessful, name='payment-success'),
#     path('payment-failed/<int:course_id>/',
#          views.PaymentFailed, name='payment-failed'),
# ]

urlpatterns = [
    path('payment/', views.payment, name='payment'),
    path('payment_ipn/', views.payment_ipn, name='payment_ipn'),
    path('payment_return/', views.payment_return, name='payment_return'),
    path('invoice/<int:order_id>/', views.invoice, name='invoice'),
    path('query/', views.query, name='query'),
]
