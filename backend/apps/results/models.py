from django.db import models
from apps.students.models import Student
from apps.courses.models import Course

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)  # e.g. '2023/2024 S1'
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2)   # A, B, C, D, F
    grade_point = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code}: {self.grade}"

class GPA(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.matric_number} - {self.semester}: {self.gpa}"
