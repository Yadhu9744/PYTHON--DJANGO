from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, ContactMessage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_featured', 'created_at')
    list_filter = ('is_featured',)
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('created_at',)
