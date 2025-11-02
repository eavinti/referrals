from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta
import time

from referrals.models import Referral
from referrals.serializers import ReferralSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=True, methods=['post'], url_path='resend')
    def resend_invitation(self, request, pk=None):
        try:
            referral = self.get_object()
        except Referral.DoesNotExist:
            return Response({"detail": "Referral not found."}, status=status.HTTP_404_NOT_FOUND)

        # 1. Business Rule: Only allow resend if status is 'Invitation Sent'
        if referral.status != 'INVITATION_SENT':
            return Response(
                {"detail": "Cannot resend invitation for a referral that is not in 'Invitation Sent' status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Business Rule: Cannot resend within 30 seconds of the last send time
        cooldown_period = timedelta(seconds=30)
        time_since_last_send = timezone.now() - referral.last_sent_at

        if time_since_last_send < cooldown_period:
            remaining_time = (cooldown_period - time_since_last_send).total_seconds()
            return Response(
                {"detail": f"Cannot resend within 30 seconds. Please wait {remaining_time:.1f} more seconds."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- Simulated Email Sending Process ---
        time.sleep(3)  # Simulate 3 seconds

        # 3. Success: Update the last_sent_at timestamp to current time
        referral.last_sent_at = timezone.now()
        referral.save(update_fields=['last_sent_at'])

        # Return updated data
        serializer = self.get_serializer(referral)
        return Response(serializer.data, status=status.HTTP_200_OK)