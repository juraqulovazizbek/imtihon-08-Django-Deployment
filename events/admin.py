from django.contrib import admin
from .models import Event, Registration


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0
    readonly_fields = ['user', 'status', 'registered_at']
    can_delete = False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'event_type', 'start_time', 'end_time',
        'capacity', 'get_registered', 'get_available', 'created_by',
    ]
    list_filter = ['event_type', 'start_time']
    search_fields = ['title', 'description', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    inlines = [RegistrationInline]

    @admin.display(description='Registered')
    def get_registered(self, obj):
        return obj.registered_count

    @admin.display(description='Available')
    def get_available(self, obj):
        return obj.available_seats


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registered_at']
    list_filter = ['status', 'registered_at']
    search_fields = ['user__email', 'event__title']
    readonly_fields = ['registered_at', 'updated_at']
    ordering = ['-registered_at']