from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='student')
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return self.username

class School(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class ClassRoom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16)
    year = models.IntegerField()

    class Meta:
        unique_together = ('code', 'year', 'school')

    def __str__(self):
        return f"{self.school.code}-{self.code}-{self.year}"

class Student(models.Model):
    id = models.CharField(primary_key=True, max_length=64)  # StudentID
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)
    admission_year = models.IntegerField()
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"

class Parent(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.CharField(max_length=32)
    score = models.DecimalField(max_digits=6, decimal_places=2)
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=100)

    def __str__(self):
        return f"{self.student.id} - {self.subject.code} - {self.term}"

class CSVUpload(models.Model):
    uploader = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=32, default='pending')
    errors = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"CSVUpload {self.filename} ({self.status})"
