from django.db import models


class Referral(models.Model):
    STATUS_CHOICES = [
        ('INVITATION_SENT', 'Invitation Sent'),
        ('APPLICATION_RECEIVED', 'Application Received'),
        ('JOINED', 'Joined'),
        ('DECLINED', 'Declined'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='INVITATION_SENT'
    )

    referred_date = models.DateTimeField(auto_now_add=True)
    last_sent_at = models.DateTimeField(auto_now_add=True)
    joined_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-referred_date']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"