from django.contrib import admin
from .models import *
from django.utils.html import mark_safe

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'price', 'quantity', 'item_total', 'order']
    list_filter = ['order']
    
@admin.register(Subscriber)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_active', 'subscribed_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('name', 'email', 'phone')
    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'text','star_display', 'created_at','photo_preview')
    search_fields = ('name', 'rating')
    list_filter = ('name', 'rating')
    def star_display(self,obj):
       return "⭐" * obj.rating
    star_display.short_description = "Rating"

    def photo_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="border-radius:8px;" />')
        return "No image"
    photo_preview.short_description = "Image"
    
@admin.register(LiquorCategory)
class LiquorCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Liquor)
class LiquorAdmin(admin.ModelAdmin):
    list_display=('name','category','image','region','vintage','price','producer')
    search_fields=('name','category','region','price','producer')
    list_filter=('name','category','region','price','producer')
    def photo_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" style="border-radius:8px;" />')
        return "No image"
    photo_preview.short_description = "Image"