from django.db import models
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count, Case, When, FloatField, F

from referrals.models import Referral


class AnalyticsAPIView(APIView):
    """
    API endpoint to return referral analytics metrics.
    """

    def get(self, request, *args, **kwargs):
        # Use Django's ORM aggregation features for efficient calculation

        # Total count of all referrals
        total_invited = Referral.objects.count()

        # Counts for specific statuses
        status_counts = Referral.objects.aggregate(
            sent_count=Count(Case(
                When(status='INVITATION_SENT', then=1),
                output_field=models.IntegerField()
            )),
            approved_count=Count(Case(
                # Approved is defined as 'Application Received' or 'Joined'
                When(status__in=['APPLICATION_RECEIVED', 'JOINED'], then=1),
                output_field=models.IntegerField()
            )),
        )

        sent_count = status_counts['sent_count']
        approved_count = status_counts['approved_count']

        # Calculate conversion rate: (Approved / Total Invited) * 100
        # Protect against division by zero
        conversion_rate = 0.0
        if total_invited > 0:
            conversion_rate = (approved_count / total_invited) * 100

        # Construct the response data
        data = {
            "total_invited": total_invited,
            "invitations_sent_count": sent_count,
            "approved_count": approved_count,
            "conversion_rate": round(conversion_rate, 2),  # Round to 2 decimal places
        }

        return Response(data, status=status.HTTP_200_OK)