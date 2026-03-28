from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Q

from .models import Event, Registration
from .serializers import (
    EventSerializer,
    RegistrationSerializer,
    EventStatSerializer,
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .filters import EventFilter


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related('created_by').all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_time', 'created_at', 'capacity']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def participants(self, request, pk=None):
        event = self.get_object()
        registrations = event.registrations.filter(
            status='REGISTERED'
        ).select_related('user')
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def stats(self, request, pk=None):
        event = self.get_object()
        return Response({
            'event_id': event.id,
            'title': event.title,
            'capacity': event.capacity,
            'registered_count': event.registered_count,
            'available_seats': event.available_seats,
            'is_registration_open': event.is_registration_open,
        })


class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['event__title', 'status']
    ordering_fields = ['registered_at']
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Registration.objects.select_related('user', 'event').all()
        return Registration.objects.select_related(
            'user', 'event'
        ).filter(user=user)

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        registration = self.get_object()

        if not request.user.is_staff and registration.user != request.user:
            return Response(
                {"detail": "You do not have permission to cancel this registration."},
                status=status.HTTP_403_FORBIDDEN
            )

        if registration.status == 'CANCELLED':
            return Response(
                {"detail": "Registration is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        registration.status = 'CANCELLED'
        registration.save()
        return Response({
            "detail": "Registration cancelled successfully.",
            "registration_id": registration.id,
            "event": registration.event.title,
            "status": registration.status,
        })


class TopEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        top_events = Event.objects.annotate(
            reg_count=Count(
                'registrations',
                filter=Q(registrations__status='REGISTERED')
            )
        ).order_by('-reg_count')[:5]

        serializer = EventStatSerializer(top_events, many=True)
        return Response({"top_5_events": serializer.data})


class AdminStatisticsView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = EventStatSerializer

    def get_queryset(self):
        return Event.objects.annotate(
            reg_count=Count(
                'registrations',
                filter=Q(registrations__status='REGISTERED')
            )
        ).order_by('-reg_count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "summary": {
                "total_events": queryset.count(),
                "total_registrations": Registration.objects.filter(
                    status='REGISTERED'
                ).count(),
                "total_cancelled": Registration.objects.filter(
                    status='CANCELLED'
                ).count(),
            },
            "events": serializer.data,
        })