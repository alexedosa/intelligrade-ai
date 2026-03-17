from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    level = models.IntegerField()  # 100, 200, 300, 400
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_number})"
