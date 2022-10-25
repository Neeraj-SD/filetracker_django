from django.shortcuts import render
import requests


# Create your views here.

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


# if you want to use Authorization Code Grant, use this
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = 'http://127.0.0.1:8000'
#     client_class = OAuth2Client

class CustomAdapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            params={"access_token": token.token, "alt": "json"},
        )
        print(resp)
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider().sociallogin_from_response(request, extra_data)
        # print('login:'+login)
        return login

class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
    adapter_class = CustomAdapter
    # client_class = OAuth2Client
    
    print('Entered here')
