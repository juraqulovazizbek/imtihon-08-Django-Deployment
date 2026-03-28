from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(lookup_expr='icontains')
    event_type = filters.ChoiceFilter(
        choices=[('ONLINE', 'Online'), ('OFFLINE', 'Offline')]
    )
    start_after = filters.DateTimeFilter(
        field_name='start_time', lookup_expr='gte'
    )
    start_before = filters.DateTimeFilter(
        field_name='start_time', lookup_expr='lte'
    )
    min_capacity = filters.NumberFilter(
        field_name='capacity', lookup_expr='gte'
    )

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'location']