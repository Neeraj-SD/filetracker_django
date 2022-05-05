from dataclasses import fields
from functools import cached_property
from django.forms import CharField
from django.http import JsonResponse
from rest_framework import serializers
from .models import Faculty, Position, Request, Student


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name']


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ['faculty', 'request', 'status', 'remarks', 'created_time']
        ordering = ['-created_time']


class CreatePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['faculty', 'request']


class RequestSerializer(serializers.ModelSerializer):

    issued_by = StudentSerializer
    issued_to = FacultySerializer
    history = serializers.SerializerMethodField()
    current_position = serializers.SerializerMethodField()

    # current_position = serializers.SerializerMethodField(
    #     method_name='get_current_position')

    class Meta:
        model = Request
        fields = ['id', 'header', 'body',
                  'issued_by', 'issued_to', 'current_position', 'history', ]

    def get_history(self, request, ):
        history = request.positions.order_by('-created_time')
        return PositionSerializer(history, many=True).data

    def get_current_position(self, request):
        current_position = request.positions.order_by('-created_time').first()
        return PositionSerializer(current_position).data


class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['header', 'body', 'issued_by', 'issued_to']

    def save(self, **kwargs):
        issued_by = self.validated_data['issued_by']
        issued_to = self.validated_data['issued_to']
        header = self.validated_data['header']
        body = self.validated_data['body']

        faculty = Faculty.objects.get(pk=issued_to.id)
        student = Student.objects.get(pk=issued_by.id)
        request = Request.objects.create(
            issued_by=student, issued_to=faculty, header=header, body=body)

        position = Position.objects.create(faculty=faculty, request=request)


class RequestActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['remarks']


class RequestForwardSerializer(serializers.ModelSerializer):

    faculty = FacultySerializer

    class Meta:
        model = Position
        fields = ['remarks', 'faculty']


class FacultyRequestSerializer(serializers.ModelSerializer):

    request = RequestSerializer()

    class Meta:
        model = Request
        fields = ['request']
