from rest_framework import serializers
from .models import Event, Registration


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    registered_count = serializers.ReadOnlyField()
    available_seats = serializers.ReadOnlyField()
    is_registration_open = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type',
            'location', 'start_time', 'end_time', 'capacity',
            'created_by', 'registered_count', 'available_seats',
            'is_registration_open', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')
        event_type = data.get('event_type')
        location = data.get('location')

        if start and end and end <= start:
            raise serializers.ValidationError(
                {"end_time": "end_time must be greater than start_time."}
            )
        if event_type == 'OFFLINE' and not location:
            raise serializers.ValidationError(
                {"location": "Location is required for OFFLINE events."}
            )
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_type = serializers.CharField(source='event.event_type', read_only=True)

    class Meta:
        model = Registration
        fields = [
            'id', 'user', 'event', 'event_title',
            'event_type', 'status', 'registered_at', 'updated_at',
        ]
        read_only_fields = ['user', 'status', 'registered_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        event = data.get('event')

        existing = Registration.objects.filter(user=user, event=event).first()
        if existing:
            if existing.status == 'REGISTERED':
                raise serializers.ValidationError(
                    "You are already registered for this event."
                )
            if existing.status == 'CANCELLED':
                raise serializers.ValidationError(
                    "You cancelled this event. Contact admin to re-register."
                )

        if event.capacity == 0:
            raise serializers.ValidationError(
                "Registration is closed. Event capacity is 0."
            )
        if event.available_seats <= 0:
            raise serializers.ValidationError(
                "No available seats for this event."
            )
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class EventStatSerializer(serializers.ModelSerializer):
    registered_count = serializers.ReadOnlyField()
    available_seats = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'event_type',
            'capacity', 'registered_count', 'available_seats',
        ]