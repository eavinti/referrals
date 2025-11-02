from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.referral_view import ReferralViewSet
from .views.analytics_view import AnalyticsAPIView

router = DefaultRouter()
router.register(r'referrals', ReferralViewSet, basename='referral')

urlpatterns = [
    path('', include(router.urls)),

    path('analytics/', AnalyticsAPIView.as_view(), name='referral-analytics'),
]
