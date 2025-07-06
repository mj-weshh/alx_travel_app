from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer, ListingDetailSerializer

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ListingDetailSerializer
        return ListingSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def available(self, request, pk=None):
        """
        Check if a listing is available for the given date range.
        Expects 'check_in' and 'check_out' as query parameters.
        """
        listing = self.get_object()
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')

        if not all([check_in, check_out]):
            return Response(
                {"error": "Both 'check_in' and 'check_out' parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            check_in = timezone.datetime.strptime(check_in, '%Y-%m-%d').date()
            check_out = timezone.datetime.strptime(check_out, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if check_in >= check_out:
            return Response(
                {"error": "Check-out date must be after check-in date"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check for overlapping bookings
        is_available = not Booking.objects.filter(
            listing=listing,
            check_out__gt=check_in,
            check_in__lt=check_out,
            status__in=['PENDING', 'CONFIRMED']
        ).exists()

        return Response({
            'is_available': is_available,
            'listing': listing.id,
            'check_in': check_in,
            'check_out': check_out
        })

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or created.
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return bookings for the authenticated user or all bookings for staff.
        """
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=user)

    def perform_create(self, serializer):
        """
        Create a new booking with the current user as the guest.
        """
        serializer.save(guest=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a booking.
        """
        booking = self.get_object()
        
        # Only the guest or staff can cancel a booking
        if booking.guest != request.user and not request.user.is_staff:
            return Response(
                {"error": "You do not have permission to cancel this booking"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if booking.status == 'CANCELLED':
            return Response(
                {"error": "This booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.status == 'COMPLETED':
            return Response(
                {"error": "Cannot cancel a completed booking"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'CANCELLED'
        booking.save()
        
        return Response({
            "message": "Booking cancelled successfully",
            "booking_id": booking.id,
            "status": booking.status
        })
