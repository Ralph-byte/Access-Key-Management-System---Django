
from django.db import models
from django.contrib.auth.models import User

class AccessKey(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked'),
    )

    personnel = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    date_of_procurement = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()

class MicroFocusAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

