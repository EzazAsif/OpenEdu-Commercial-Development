from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount
from django.http import Http404

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

