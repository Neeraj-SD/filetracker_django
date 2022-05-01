from django.contrib import admin
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
    list_display = ['first_name', 'last_name', 'department']
