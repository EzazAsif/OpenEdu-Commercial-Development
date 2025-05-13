from social_django.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User

@receiver(pre_social_login)
def social_user_connected(sender, request, socialauth, **kwargs):
    """Link social account to existing user or create a new user."""
    UserModel = get_user_model()  # Get the custom user model

    # If the user already exists, we associate the social account with them
    if socialauth.is_existing:
        return

    # If the user doesn't exist, create a new user using the social auth data
    if socialauth.provider == 'google':
        email = socialauth.extra_data.get('email')
        username = email.split('@')[0]  # Generate username from email
        first_name = socialauth.extra_data.get('name')
        # Create a new user and link it to the social account
        user = UserModel.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            password=None  # Don't set a password, as this is for social login
        )
        socialauth.user = user
        socialauth.save()

@receiver(pre_social_login)
def social_user_connected(sender, request, socialauth, **kwargs):
    """Link social account to existing user or create a new user."""
    UserModel = get_user_model()  # Get the custom user model

    # If the user already exists, we associate the social account with them
    if socialauth.is_existing:
        return

    # If the user doesn't exist, create a new user using the social auth data
    if socialauth.provider == 'google':
        email = socialauth.extra_data.get('email')
        username = email.split('@')[0]  # Generate username from email
        first_name = socialauth.extra_data.get('name')
        last_name = socialauth.extra_data.get('family_name', '')
        picture_url = socialauth.extra_data.get('picture', '')  # Google profile picture

        # Create a new user and link it to the social account
        user = UserModel.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=None  # Don't set a password, as this is for social login
        )
        # Save the picture URL or other info to the user model
        user.profile_picture = picture_url
        user.save()

        socialauth.user = user
        socialauth.save()
