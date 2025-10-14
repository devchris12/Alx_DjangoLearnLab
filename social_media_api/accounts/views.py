from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile


@login_required
def follow_user(request, user_id):
    """
    TASK: Develop views in the accounts app that allow users to follow and unfollow others
    View to follow a user. Updates the following relationship.
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Prevent users from following themselves
    if request.user == user_to_follow:
        messages.error(request, "You cannot follow yourself.")
        return redirect('blog:profile', username=request.user.username)
    
    # Get or create profiles
    current_profile = request.user.profile
    profile_to_follow = user_to_follow.profile
    
    # Follow the user
    if not current_profile.is_following(profile_to_follow):
        current_profile.follow(profile_to_follow)
        messages.success(request, f"You are now following {user_to_follow.username}.")
    else:
        messages.info(request, f"You are already following {user_to_follow.username}.")
    
    return redirect('blog:profile', username=user_to_follow.username)


@login_required
def unfollow_user(request, user_id):
    """
    TASK: Develop views in the accounts app that allow users to follow and unfollow others
    View to unfollow a user. Updates the following relationship.
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    
    # Get profiles
    current_profile = request.user.profile
    profile_to_unfollow = user_to_unfollow.profile
    
    # Unfollow the user
    if current_profile.is_following(profile_to_unfollow):
        current_profile.unfollow(profile_to_unfollow)
        messages.success(request, f"You have unfollowed {user_to_unfollow.username}.")
    else:
        messages.info(request, f"You are not following {user_to_unfollow.username}.")
    
    return redirect('blog:profile', username=user_to_unfollow.username)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CustomUser

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(user_to_follow)
        return Response({"message": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_unfollow:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(user_to_unfollow)
        return Response({"message": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
