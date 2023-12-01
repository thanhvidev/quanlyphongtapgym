from django import views
from django.conf import settings
from django.urls import path, include
from . import views
import Carts.views
from Carts.views import add_to_cart
from django.conf.urls.static import static

urlpatterns = [
    path('add_to_cart/<int:course_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/',
         Carts.views.remove_from_cart, name='remove_from_cart'),
    path('cart/', Carts.views.cart, name='cart'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
