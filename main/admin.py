from django.contrib import admin
from .models import Mall, Product, UserProfile

# Register your models here.
admin.site.register(Mall)
admin.site.register(Product)
admin.site.register(UserProfile)
