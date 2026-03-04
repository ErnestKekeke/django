from django.contrib import admin
from .models import Product, Order, OrderItem

# Register multiple models at once
admin.site.register([
    Product,
    Order,
    OrderItem
])

