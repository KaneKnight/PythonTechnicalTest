from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bond

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = ('isin', 'size', 'currency', 'maturity', 'lei', 'legal_name', 'userid')

    def create(self, validated_data):
        return Bond.objects.create(**validated_data)            