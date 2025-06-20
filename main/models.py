from django.db import models
from django.contrib.auth.models import User

class Mall(models.Model):
    MALL_TYPE_CHOICES = [
        ("مطاعم", "مطاعم"),
        ("صيدلية", "صيدلية"),
        ("سوبر ماركت", "سوبر ماركت"),
        ("غير ذلك", "غير ذلك"),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='mall_images/', blank=True, null=True)
    working_hours = models.CharField(max_length=255)
    governorate = models.CharField(max_length=100)
    mall_type = models.CharField(max_length=20, choices=MALL_TYPE_CHOICES)

    def __str__(self):
        return self.name

class Product(models.Model):
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
