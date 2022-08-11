from django.shortcuts import render

# Create your views here.

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


# if you want to use Authorization Code Grant, use this
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = 'http://127.0.0.1:8000'
#     client_class = OAuth2Client

class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    
    print('Entered here')
