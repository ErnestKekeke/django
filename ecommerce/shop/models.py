from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)

    # Note: python -m pip install Pillow, to use image field 
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True)  # snapshot
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    product_name = models.CharField(max_length=100, blank=True)
    order_by = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.name
        if not self.order_by:
            self.order_by = self.order.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.order.id} → {self.product_name} ({self.quantity} pcs)"
