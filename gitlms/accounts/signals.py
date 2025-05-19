import re
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount

@receiver(user_logged_in)
def social_user_connected(sender, request, user, **kwargs):
    """Ensure first_name and last_name are always set, using social data or email."""

    try:
        # Try to get associated social account
        social_account = SocialAccount.objects.get(user=user)

        if user.username != user.email:
            user.username = user.email

            # Try to extract names from social data
            first_name = social_account.extra_data.get('first_name', '').strip()
            last_name = social_account.extra_data.get('family_name', '').strip()

            # If social data missing, fallback to email
            if not first_name or not last_name:
                local_part = user.email.split('@')[0]  # e.g., asifrtafid8399

                # Remove trailing numbers (e.g., 8399)
                clean_part = re.split(r'\d+', local_part)[0]  # "asifrtafid"

                # Try common delimiters first
                tokens = re.split(r'[._\-]', clean_part)

                if len(tokens) >= 2:
                    first_name = first_name or tokens[0].capitalize()
                    last_name = last_name or ' '.join(t.capitalize() for t in tokens[1:])
                else:
                    # If still one word, split in the middle
                    half = len(clean_part) // 2
                    first_name = first_name or clean_part[:half].capitalize()
                    last_name = last_name or clean_part[half:].capitalize()

            # Final fallback (just in case)
            first_name = first_name or "User"
            last_name = last_name or "Unknown"

            # Assign to user
            user.first_name = first_name
            user.last_name = last_name

            # Set profile picture if available
            user.profile_picture = social_account.extra_data.get('picture', '')

            user.save()

    except SocialAccount.DoesNotExist:
        pass  # Not a social login
