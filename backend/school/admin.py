from django.contrib import admin
from .models import User, School, ClassRoom, Student, Parent, Subject, Mark, CSVUpload

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'year', 'school')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'classroom', 'admission_year')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'score')

@admin.register(CSVUpload)
class CSVUploadAdmin(admin.ModelAdmin):
    list_display = ('filename', 'uploader', 'uploaded_at', 'status')
