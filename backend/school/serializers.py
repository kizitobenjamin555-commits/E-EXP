from rest_framework import serializers
from .models import Student, CSVUpload

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CSVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVUpload
        fields = ['id', 'filename', 'uploaded_at', 'status', 'errors']
