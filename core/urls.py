
from django.urls import path, include
from .views import GoogleLogin


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('google', GoogleLogin.as_view(), name='google_login'),
    # path('/', include('dj_rest_auth.urls')),
    # path('/registration/', include('dj_rest_auth.registration.urls')),
    # path('/login/', include('dj_rest_auth.login.urls')),

]
