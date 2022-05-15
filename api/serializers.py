from django.db import transaction
from rest_framework import serializers
from .models import CurrentPosition, Department, Faculty, Position, Request, Role, Student


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']


class FacultySerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    role = RoleSerializer()

    class Meta:
        model = Faculty
        # fields = ['name']
        fields = ['name', 'department', 'role']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name']


class SimplePositionSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = Position
        fields = ['faculty',  'status', 'remarks', 'created_time']
        # ordering =


class PositionSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()

    class Meta:
        model = Position
        fields = ['faculty',  'status', 'remarks', 'created_time']
        ordering = ['-created_time']


class CreatePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['faculty', 'request']


class RequestSerializer(serializers.ModelSerializer):

    issued_by = StudentSerializer()
    issued_to = FacultySerializer()
    current_position = SimplePositionSerializer(
        source='current_position.position')
    history = PositionSerializer(many=True, source='positions')

    class Meta:
        model = Request
        fields = ['id', 'header', 'body', 'created_time',
                  'issued_by', 'issued_to', 'current_position', 'history']


class CreateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['header', 'body', 'issued_by', 'issued_to']

    def save(self, **kwargs):
        with transaction.atomic():
            issued_by = self.validated_data['issued_by']
            issued_to = self.validated_data['issued_to']
            header = self.validated_data['header']
            body = self.validated_data['body']

            faculty = Faculty.objects.get(pk=issued_to.id)
            student = Student.objects.get(pk=issued_by.id)
            request = Request.objects.create(
                issued_by=student, issued_to=faculty, header=header, body=body)

            position = Position.objects.create(
                faculty=faculty, request=request)

            CurrentPosition.objects.create(request=request, position=position)


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


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = '__ALL__'
