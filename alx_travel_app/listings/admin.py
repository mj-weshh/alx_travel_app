from django.contrib import admin
from .models import Listing, Booking

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'country', 'price_per_night', 'is_available', 'owner')
    list_filter = ('is_available', 'property_type', 'city', 'country')
    search_fields = ('title', 'description', 'address', 'city', 'country')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ()
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'property_type')
        }),
        ('Location', {
            'fields': ('address', 'city', 'country')
        }),
        ('Details', {
            'fields': ('price_per_night', 'bedrooms', 'bathrooms', 'max_guests', 'amenities')
        }),
        ('Status', {
            'fields': ('is_available', 'owner')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'guest', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('listing__title', 'guest__username', 'guest__email')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('listing', 'guest', 'check_in', 'check_out', 'total_price')
        return self.readonly_fields
