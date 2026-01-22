from decimal import Decimal
from django.db import models
from django.contrib.auth.models  import User,AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15,blank=True)
class WaterOrder(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('processing','Processing'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled')
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='water_orders')
    quantity = models.PositiveIntegerField(help_text="Water quantity in Litres")
    phone = models.CharField(max_length=20)
    delivery_address = models.TextField()
    price_per_litre = models.DecimalField(max_digits=10,decimal_places=3,default=50.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    

    def save(self, *args, **kwargs):
        """Calculate total price before saving"""
        # Calculate total
        self.total_price = Decimal(str(self.quantity)) * self.price_per_litre
        # Call parent save method
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.quantity}L"
    
    class Meta:
        ordering = ['-order_date']





