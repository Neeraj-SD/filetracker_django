from cgitb import lookup
from urllib import request
from . import views
from django.urls import include, path

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('requests', views.RequestViewSet,
                basename='requests')
router.register('faculty/requests', views.FacultyRequestViewSet,
                basename='faculty-requests')
router.register('student/requests', views.StudentRequestViewSet,
                basename='student-requests')
# router.register('requests/<int:pk>/approve',
#                 views.RequestApproveViewSet, basename='request-approve')

request_router = routers.NestedDefaultRouter(
    router, 'requests', lookup='request')
request_router.register(
    'approve', views.RequestActionViewSet, basename='request-approve')
request_router.register(
    'reject', views.RequestActionViewSet, basename='request-reject')
request_router.register(
    'forward', views.RequestActionViewSet, basename='request-forward')

urlpatterns = router.urls + request_router.urls
