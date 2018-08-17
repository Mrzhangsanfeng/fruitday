
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url('^addcart', add_cart, name='add_cart'),
    url('^cart', cart_info, name='cart'),
    url('^order', order, name='order'),
    url('^addorder', add_order, name='addorder'),
    url('^showorder', show_order, name='showorder'),
    url('^deletecart', delete_cart, name='deletecart'),
]
