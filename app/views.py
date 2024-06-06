from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Friend
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import LoginSerializer, SignupSerializer, FriendSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .mixins import RateLimitFriendRequestsMixin
from rest_framework.pagination import PageNumberPagination

class Signup(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower()
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchFriend(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_string = request.query_params.get('st', None)
        print(search_string)

        if not search_string:
            return Response({"detail": "Query parameter 'st' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for exact email match
        exact_email_match = User.objects.filter(email=search_string)
        if exact_email_match.exists():
            # If there is an exact email match, return that user
            serializer = UserSerializer(exact_email_match, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Otherwise, search for substring in first_name or last_name
        results = User.objects.filter(username__icontains=search_string
        )

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_results = paginator.paginate_queryset(results, request)

        # Serialize the results
        serializer = UserSerializer(paginated_results, many=True)
        return paginator.get_paginated_response(serializer.data)

class FriendSuggestions(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        current_user = request.user

        # Get all friend relationships involving the current user
        friends_and_requests = Friend.objects.filter(
        Q(user=current_user) | Q(friend=current_user)
        ).values_list('friend_id', 'user_id')

        # Flatten the list of user IDs involved in friendships and friend requests
        friends_and_requests_ids = set([item for sublist in friends_and_requests for item in sublist])

        # Get all users excluding the current user and those who are already friends or have pending friend requests
        users_without_requests = User.objects.exclude(
        id__in=friends_and_requests_ids
        ).exclude(id=current_user.id)

        # Manually apply pagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(users_without_requests, request)
        serializer = UserSerializer(result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

class SendFriendRequest(RateLimitFriendRequestsMixin, APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,id):
        rate_limit_response = self.check_rate_limit(request)
        if rate_limit_response:
            return rate_limit_response
        try:
            user = User.objects.filter(id=id).first()
            if(user == request.user):
                return Response({'error': 'Invalid User Id'}, status=status.HTTP_400_BAD_REQUEST)
            friend = Friend.objects.get_or_create(user=user, friend = request.user)
            return Response({"Message":"Friend Request Sent"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid User Id'}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequests(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        requests = Friend.objects.filter(user=request.user, is_accepted=False)
        # Manually apply pagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(requests, request)
        serializer = FriendSerializer(result_page,many=True)
        return paginator.get_paginated_response(serializer.data)
    
class AcceptFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,id):
        friend = Friend.objects.filter(id=id).first()
        if friend is not None:
            friend.is_accepted = True
            friend.save()
            return Response({"Message":"Friend Request Accepted"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"Message":"Friend Request Doesnot Exist"}, status=status.HTTP_400_BAD_REQUEST)

class RejectFriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self,request,id):
        friend = Friend.objects.filter(id=id).first()
        if friend is not None:
            friend.delete()
            return Response({"Message":"Friend Request Rejected"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Message":"Friend Request Doesnot Exist"}, status=status.HTTP_400_BAD_REQUEST)

class Friends(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        friends = Friend.objects.filter(user = request.user, is_accepted=True)
        # Manually apply pagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(friends, request)
        serializer = FriendSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)