from dataclasses import field
from rest_framework import serializers
from .models import UserModel

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user
    class Meta:
        model = UserModel
        fields = ["username","password","nickname","profile_url"]
        extra_kwargs = {
            'password' : {'write_only' : True}
        }