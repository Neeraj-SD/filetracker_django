from django.db import models

# Create your models here.


class Batch(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT)
    admission_number = models.CharField(max_length=255)
    register_number = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Faculty(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Request(models.Model):
    issued_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    body = models.CharField(max_length=3000)
    created_time = models.DateTimeField(auto_now_add=True)


class Position(models.Model):
    STATUS_PENDING = 'P'
    STATUS_FORWARDED = 'F'
    STATUS_REJECTED = 'R'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_FORWARDED, 'Forwarded'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_time = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=3000)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
