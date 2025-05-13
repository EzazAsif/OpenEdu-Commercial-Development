from allauth.account.adapter import DefaultAccountAdapter
from .models import User

class CustomAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup( request,sociallogin):
        print(request,sociallogin)
        """
        By overriding this method, you can skip the sign-up page
        and directly log in the user if the email already exists.
        """
        email = sociallogin.user.email
        try:
            user = User.objects.get(email=email)
            # If the user already exists, return False to skip signup and log them in
            return False
        except User.DoesNotExist:
            return True
