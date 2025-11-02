from rest_framework import serializers
from django.utils import timezone

from .models import Referral


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ['id', 'first_name', 'last_name', 'email', 'status', 'referred_date', 'last_sent_at', 'joined_date']
        read_only_fields = ['id', 'referred_date', 'last_sent_at']

    def validate_email(self, value):
        email = value.strip().lower()

        if self.instance is None and Referral.objects.filter(email=email).exists():
            raise serializers.ValidationError("A referral with this email already exists.")
        return email

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].lower().strip()
        return Referral.objects.create(**validated_data)

    def update(self, instance, validated_data):
        current_status = instance.status
        new_status = validated_data.get('status', current_status)

        STATUS_ORDER = {
            'INVITATION_SENT': 0,
            'APPLICATION_RECEIVED': 1,
            'JOINED': 2,
            'DECLINED': 3
        }

        if new_status == 'JOINED' and current_status != 'JOINED':
            instance.joined_date = timezone.now()
        elif new_status != 'JOINED' and current_status == 'JOINED':
            instance.joined_date = None

        if current_status != new_status:
            current_order = STATUS_ORDER.get(current_status)
            new_order = STATUS_ORDER.get(new_status)

            if new_order is not None and current_order is not None:
                if new_order < current_order:
                    raise serializers.ValidationError(
                        f"Cannot move status backward from '{current_status}' to '{new_status}'."
                    )

        return super().update(instance, validated_data)