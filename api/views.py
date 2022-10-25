from http.client import BAD_REQUEST, NOT_FOUND
from multiprocessing import context
from pprint import pprint
import uuid
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated

from filetracker_django.settings import AUTH_USER_MODEL

from .serializers import CreatePositionSerializer, CreateRequestSerializer, FacultyRequestSerializer, HistorySerializer, PositionSerializer, RequestForwardSerializer, RequestSerializer, RequestActionSerializer
from .models import CurrentPosition, Faculty, Position, Request
# Create your views here.

# class UserViewSet(ModelViewSet):
#     queryset = Request.objects.all()
#     serializer_class

class RequestViewSet(ModelViewSet):
    # queryset = Request.objects \
    #     .filter(issued_by__user=)
    #     .select_related(
    #         'issued_to__department', 'issued_to',
    #         'issued_by', 'current_position__position__faculty__department',
    #     ) \
    #     .prefetch_related(
    #          'positions__faculty__department'
    #     ) \
    #     .all()
    
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def history(self, request, pk):

        positions = Position.objects.filter(
            request_id=pk).order_by('-created_time').all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Request.objects \
                                .filter(issued_by__user=self.request.user.id) \
                                .select_related(
                                    'issued_to__department', 'issued_to',
                                    'issued_by', 'current_position__position__faculty__department',
                                ) \
                                .prefetch_related(
                                    'positions__faculty__department'
                                ) \
                                .all() 
        return queryset

    def get_serializer_class(self):
        # if self.request.method == 'GET':
        #     print(self.request.user.id)
        if self.request.method == 'POST':
            return CreateRequestSerializer
        return RequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateRequestSerializer(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        request = serializer.save()

        return Response(serializer.data)

def validate_uuid(uuid):
    try:
            print(uuid.UUID(uuid, version=4))
            return True
    except:
        return False

class RequestActionViewSet(CreateModelMixin, GenericViewSet):
    lookup_field = 'uuid'
    http_method_names = ['post']

    def get_serializer_class(self):
        action = self.request.path.split("/")[-2]

        if action == 'forward':
            return RequestForwardSerializer
        return RequestActionSerializer

    # queryset = Position.objects.all()


    def create(self, request, *args, **kwargs):
        print(request.path)

        action = request.path.split("/")[-2]

        
        if not validate_uuid(self.kwargs['request_pk']):
           return Response('Invalid request id.')

        request_uid = uuid.UUID(self.kwargs['request_pk'])

        # request = Request.objects.ge
        request = Request.objects.get(uuid=request_uid)



        position = Position.objects \
            .filter(request_id=request.id) \
            .order_by('-created_time') \
            .first()
        if position is None:
            return Response('Invalid request id.')

        if not action == 'forward':

            if action == 'approve':
                position.status = 'A'
            elif action == 'reject':
                position.status = 'R'
            else:
                return Response(NOT_FOUND)

            position.remarks = request.data['remarks']
            position.save()
            serializer = RequestActionSerializer(position)
            return Response(serializer.data)

        else:

            faculty = Faculty.objects.filter(
                pk=request.data['faculty'])
            print(faculty)
            if not faculty.exists():
                return Response('Invalid faculty id to send to.')

            position.remarks = request.data['remarks']
            position.status = 'F'
            position.save()

            position = Position.objects.create(
                faculty=faculty.get(), request_id=request.id)

            CurrentPosition.objects.filter(request_id=request.id).update(
                position=position)

            serializer = RequestForwardSerializer(position)
            return Response(serializer.data)


@permission_classes([IsAuthenticated])
class FacultyRequestViewSet(ModelViewSet):
    serializer_class = FacultyRequestSerializer

    request_classes = ['GET']    
    
    def get_queryset(self):
        queryset = Position.objects.filter(faculty__user=self.request.user.id).select_related(
        'request', 'request__issued_to', 'request__issued_by') \
        .prefetch_related('request__positions') \
        .order_by('-created_time') \
        .all()
        return queryset   
    


class StudentRequestViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = RequestSerializer

    http_methods = ['get']

    def get_queryset(self):
        return  Request.objects \
                                .filter(issued_by__user=self.request.user.id) \
                                .select_related \
                                ( 
                                'issued_to__department',  'issued_to',
                                'issued_by', 'current_position__position__faculty__department',
                                ) \
                                .prefetch_related( 'positions__faculty__department') \
                                .all()


