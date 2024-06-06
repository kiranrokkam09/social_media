from django.urls import path
from . import views

urlpatterns = [
    path("signup",views.Signup.as_view(),name="signup"),
    path("login",views.Login.as_view(),name="login"),
    path("suggestions",views.FriendSuggestions.as_view(),name="FriendSuggestions"),
    path("search/",views.SearchFriend.as_view(),name="SearchFriend"),
    path("sendrequest/<int:id>",views.SendFriendRequest.as_view(),name="SendFriendRequest"),
    path("requests",views.FriendRequests.as_view(),name="FriendRequests"),
    path("acceptrequest/<int:id>",views.AcceptFriendRequest.as_view(),name="AcceptFriendRequest"),
    path("rejectrequest/<int:id>",views.RejectFriendRequest.as_view(),name="RejectFriendRequest"),
    path("friends",views.Friends.as_view(),name="friends"),
]