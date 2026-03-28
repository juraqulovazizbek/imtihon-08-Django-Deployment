from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet,
    RegistrationViewSet,
    TopEventsView,
    AdminStatisticsView,
)

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'registrations', RegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/top-events/', TopEventsView.as_view(), name='top-events'),
    path('admin/statistics/', AdminStatisticsView.as_view(), name='admin-statistics'),
]