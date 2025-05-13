from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from django.http import Http404
import logging

# Set up logging
logger = logging.getLogger(__name__)

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin=None):
        if sociallogin is None:
            # Manually get sociallogin from request (this is more of a fallback for your case)
            sociallogin = request.socialaccount
        if not sociallogin:
            raise Http404("No social login found")

        # If the user is already existing, do nothing
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                # Attempt to find the existing user by email
                user = User.objects.get(email=email)
                sociallogin.user = user  # Link this social login to the user

                # Save the social account so the link persists in future logins
                sociallogin.save()

                # Optionally, you can create a SocialAccount if it doesn't exist
                social_account, created = SocialAccount.objects.get_or_create(user=user, provider=sociallogin.account.provider)
                if created:
                    social_account.save()

            except User.DoesNotExist:
                pass  # Do nothing if user doesn't exist

    def new_user(self, request, sociallogin):
        """
        Override to properly pass `sociallogin` when creating a new user.
        """
        if sociallogin is None:
            logger.error("sociallogin is not passed correctly!")
            raise Exception("sociallogin is not passed correctly!")

        # Debugging line to log the sociallogin object
        logger.debug(f"Sociallogin: {sociallogin}")  # Log sociallogin

        # Call the parent method to create the user and pass the sociallogin
        user = super().new_user(request, sociallogin)

        # Link the social login to the newly created user
        sociallogin.user = user
        sociallogin.save()  # Save the sociallogin object to persist the link

        # Log the user creation
        logger.debug(f"Created user: {user}")

        return user
