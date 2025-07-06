from rest_framework import serializers
from .models import Listing, Booking
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class ListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'status')
    
    def validate(self, data):
        """
        Check that check_in is before check_out and the listing is available
        """
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(
            listing=data['listing'],
            check_out__gt=data['check_in'],
            check_in__lt=data['check_out'],
            status__in=['PENDING', 'CONFIRMED']
        )
        
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)
            
        if overlapping_bookings.exists():
            raise serializers.ValidationError("This listing is already booked for the selected dates")
            
        return data

class ListingDetailSerializer(ListingSerializer):
    """
    Serializer for the Listing model with additional details
    """
    bookings = BookingSerializer(many=True, read_only=True)
    
    class Meta(ListingSerializer.Meta):
        fields = [f.name for f in Listing._meta.get_fields() if not f.is_relation or f.many_to_one] + ['bookings']
