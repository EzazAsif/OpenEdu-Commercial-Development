from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from social_django.models import UserSocialAuth

@receiver(user_logged_in)
def social_user_connected(sender, request, user, **kwargs):
    """Link social account to existing user or create a new user in custom model."""
    
    # We only want to handle social login users
    try:
        # Retrieve the social authentication user associated with the logged-in user
        social_user = UserSocialAuth.objects.get(user=user)

        # Only update if the username is not set (to avoid overwriting if already set)
        if user.username != user.email:
            # Update the username to be the user's email
            user.username = user.email  # Set username to the user's email
            user.first_name = social_user.extra_data.get('first_name', '')  # Get first name from social data
            user.last_name = social_user.extra_data.get('family_name', '')  # Use family_name for last name
            
            # Optionally, store other fields like the profile picture URL
            user.profile_picture = social_user.extra_data.get('picture', '')  # Save profile picture from Google data

            # Save the updated user information
            user.save()

    except UserSocialAuth.DoesNotExist:
        # User did not log in through social auth, do nothing
        pass
