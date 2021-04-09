from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added, social_account_updated, social_account_removed
from allauth.socialaccount.models import SocialAccount, SocialToken
from .models import Profile
import re


@receiver(user_signed_up)
def signed_up(user, **kwargs):
    social_info = SocialAccount.objects.filter(user=user)[0]
    social_token = SocialToken.objects.filter(account=social_info)[0]
    if social_info.provider == "google":
        if social_info.extra_data["hd"] == "iniad.org":
            match = re.match(r"s1f10(([0-9]{2})[0-9]{4})[0-9]{1}@iniad\.org", social_info.extra_data["email"])
            if match:
                try:
                    profile = Profile.objects.get(email=social_info.extra_data["email"])
                    user.profile = profile
                except Profile.DoesNotExist:
                    user.profile = None
    print(user)
    user.save()


@receiver(social_account_added)
def account_added(request, sociallogin, **kwargs):
    user = request.user
    social_info = sociallogin.account
    social_token = sociallogin.token
    if social_info.provider == "google":
        if social_info.extra_data["hd"] == "iniad.org":
            match = re.match(r"s1f10(([0-9]{2})[0-9]{4})[0-9]{1}@iniad\.org", social_info.extra_data["email"])
            if match:
                try:
                    profile = Profile.objects.get(email=social_info.extra_data["email"])
                    user.profile = profile
                except Profile.DoesNotExist:
                    user.profile = None
            print(user)
            user.save()