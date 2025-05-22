from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ("undone", "Undone"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.CharField(max_length=50)
    telegram_user_id = models.BigIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="undone")

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
