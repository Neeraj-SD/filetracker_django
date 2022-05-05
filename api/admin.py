from select import select
from django.contrib import admin
from django.http import HttpRequest
from . import models

# Register your models here.


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'department', 'batch']
    autocomplete_fields = ['department', 'batch']
    # search_fields = ['department', 'batch']


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(models.Faculty)
class FaculyAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'department', 'role']
    search_fields = ['first_name', 'last_name']
    list_select_related = ['department', 'role']


@admin.register(models.Request)
class RequestAdmin(admin.ModelAdmin):

    def get_queryset(self, request: HttpRequest):
        return models.Request.objects.prefetch_related('positions').all()

    list_display = ['header', 'body', 'issued_by',
                    'issued_to', 'position']
    # list_select_related = ['issued_by', 'issued_to']

    def status(self, positions):
        return positions.order_by('-created_time').first().get_status_display()

    def position(self, request):
        return request.positions.order_by('-created_time').first().faculty.role


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['request', 'faculty', 'status', 'created_time', 'remarks']
    autocomplete_fields = ['faculty']


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
