from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Email(models.Model):
    sender = models.ForeignKey(User, related_name='sent_emails', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_emails', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body_encrypted = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.recipient} - {self.subject}"