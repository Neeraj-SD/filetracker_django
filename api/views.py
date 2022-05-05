from http.client import BAD_REQUEST, NOT_FOUND
from pprint import pprint
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response

from .serializers import CreatePositionSerializer, CreateRequestSerializer, FacultyRequestSerializer, PositionSerializer, RequestForwardSerializer, RequestSerializer, RequestActionSerializer
from .models import CurrentPosition, Faculty, Position, Request
# Create your views here.


class RequestViewSet(ModelViewSet):
    queryset = Request.objects \
        .select_related(
            'issued_to__department', 'issued_to__role', 'issued_to',
            'issued_by', 'current_position__position__faculty__department',
            'current_position__position__faculty__role'
        ) \
        .prefetch_related(
            'positions__faculty__role', 'positions__faculty__department'
        ) \
        .all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateRequestSerializer
        return RequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request = serializer.save()

        return Response(serializer.data)


class RequestActionViewSet(CreateModelMixin, GenericViewSet):
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

        request_id = self.kwargs['request_pk']

        # request = Request.objects.ge

        position = Position.objects \
            .filter(request_id=request_id) \
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
                faculty=faculty.get(), request_id=request_id)

            CurrentPosition.objects.filter(request_id=request_id).update(
                position=position)

            serializer = RequestForwardSerializer(position)
            return Response(serializer.data)


class FacultyRequestViewSet(ModelViewSet):
    serializer_class = FacultyRequestSerializer

    queryset = Position.objects.filter(faculty=1).select_related(
        'request', 'request__issued_to', 'request__issued_by') \
        .prefetch_related('request__positions') \
        .order_by('-created_time') \
        .all()


class StudentRequestViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = RequestSerializer

    http_methods = ['get']

    queryset = Request.objects.select_related(
        'issued_to__department', 'issued_to__role', 'issued_to',
        'issued_by', 'current_position__position__faculty__department',
        'current_position__position__faculty__role') \
        .prefetch_related('positions__faculty__role', 'positions__faculty__department') \
        .all()
