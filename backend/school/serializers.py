from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # placeholder; original StudentSerializer remains in models context
        fields = '__all__'

class CSVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ['id', 'filename', 'uploaded_at', 'status', 'errors', 'created_count', 'updated_count', 'processed_at']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value

    def validate_new_password(self, value):
        # Additional password policy checks can be added here
        return value
