# mixins.py
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from .models import Friend

class RateLimitFriendRequestsMixin:
    def check_rate_limit(self, request):
        current_time = timezone.now()
        one_minute_ago = current_time - timedelta(minutes=1)
        friend_requests_count = Friend.objects.filter(
            friend=request.user,
            created_at__gte=one_minute_ago
        ).count()

        if friend_requests_count >= 3:
            return JsonResponse({'error': 'You can only send 3 friend requests per minute.'}, status=429)
        return None
