from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Listing(models.Model):
    PROPERTY_TYPES = [
        ('HOUSE', 'House'),
        ('APARTMENT', 'Apartment'),
        ('HOTEL', 'Hotel'),
        ('VILLA', 'Villa'),
        ('CABIN', 'Cabin'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    max_guests = models.PositiveIntegerField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    amenities = models.JSONField(default=list, blank=True)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.city}, {self.country}"

    class Meta:
        ordering = ['-created_at']

class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('CONFIRMED', 'Confirmed'),
            ('CANCELLED', 'Cancelled'),
            ('COMPLETED', 'Completed'),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.guest.email} - {self.listing.title} ({self.check_in} to {self.check_out})"

    class Meta:
        ordering = ['-created_at']
