from django.contrib.auth.models import User
from django.db import models

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
        indexes = [
            models.Index(fields=['user', 'friend']),
        ]

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username} - Accepted: {self.is_accepted}"
