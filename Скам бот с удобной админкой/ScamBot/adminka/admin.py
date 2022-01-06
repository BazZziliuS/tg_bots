from django.contrib import admin
from .models import User, Category, Item


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Item)