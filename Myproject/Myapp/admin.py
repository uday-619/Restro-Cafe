from django.contrib import admin
from .models import MenuItem, Order, SeatReservation, Profile

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name',)
    list_editable = ('is_available',)  # Allows toggle directly from the list view

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'item__name')

@admin.register(SeatReservation)
class SeatReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'seat_code', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'seat_code')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

