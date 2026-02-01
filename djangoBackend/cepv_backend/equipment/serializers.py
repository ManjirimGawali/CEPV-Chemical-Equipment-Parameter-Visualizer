from rest_framework import serializers
from .models import Dataset
from django.contrib.auth.models import User
class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = [
            'id',
            'name',
            'filename',
            'uploaded_at',
            'preview',
            'charts',
            'summary'
        ]

class SignUpSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self,validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            password=validate_data['password']
        )
        return user