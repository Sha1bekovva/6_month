from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver

@receiver(social_account_added)
def populate_user_profile(request, sociallogin, **kwargs):
    user = sociallogin.user
    data = sociallogin.account.extra_data

    user.first_name = data.get('given_name', '')
    user.last_name = data.get('family_name', '')
    user.avatar = data.get('picture', '')
    user.save()
