from urllib import request
from django.db import models
from django.conf import settings
import uuid as uuid_lib

# Create your models here.


class Batch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)


    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


# class Role(models.Model):
#     name = models.CharField(max_length=255)

#     class Meta:
#         ordering = ['id']

#     def __str__(self) -> str:
#         return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT,null=True)
    phone_number = models.CharField(max_length=255)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, null=True)
    admission_number = models.CharField(max_length=255)
    register_number = models.CharField(max_length=255)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)    

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Faculty(models.Model):
    ROLE_HOD = 'HD'
    ROLE_SENIOR_ADVISOR = 'SA'
    ROLE_ADVISOR = 'AR'
    ROLE_TEACHING = 'TG'
    ROLE_NON_TEACHING = 'NT'
    STATUS_CHOICES = [
        (ROLE_HOD, 'HOD'),
        (ROLE_SENIOR_ADVISOR, 'Senior Advisor'),
        (ROLE_ADVISOR, 'Advisor'),
        (ROLE_TEACHING, 'Teaching'),
        (ROLE_NON_TEACHING, 'Non Teaching'),
    ]




    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True)
    phone_number = models.CharField(max_length=255)
    # role = models.ForeignKey(
    #     Role, on_delete=models.PROTECT, null=True, blank=True)
    role = models.CharField(max_length=2, choices= STATUS_CHOICES)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)        

    def name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Request(models.Model):
    issued_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    body = models.CharField(max_length=3000)
    created_time = models.DateTimeField(auto_now_add=True)
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)

    def __str__(self) -> str:
        return f'{self.id}'


class Position(models.Model):
    STATUS_PENDING = 'P'
    STATUS_FORWARDED = 'F'
    STATUS_REJECTED = 'R'
    STATUS_APPROVED = 'A'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_FORWARDED, 'Forwarded'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_time = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=3000, blank=True)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name='positions')
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)    

    def get_status(self):
        return self.status


class CurrentPosition(models.Model):
    request = models.OneToOneField(
        Request, on_delete=models.CASCADE, related_name='current_position')
    position = models.OneToOneField(Position, on_delete=models.CASCADE)
    
    uuid = models.UUIDField(
    db_index=True,
    default=uuid_lib.uuid4,
    editable=False)

    def __str__(self) -> str:
        return self.position
