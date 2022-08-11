from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import Faculty, Student
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_student_or_faculty_for_new_user(sender, **kwargs):
    if kwargs['created']:
        user_id = kwargs['instance']
        print('user_id: ',user_id)
        user = get_user_model().objects.get(email=user_id)
        print('user: ',user)
        # Student.objects.create(user=user_id)
        # user = settings.AUTH_USER_MODEL.objects.find()
        if user.is_faculty:
            Faculty.objects.create(user=user_id)
        else:
            Student.objects.create(user=user_id)
