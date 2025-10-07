from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "name", "email", "role", "phone", "address",
            "wallet_balance", "loyalty_points",
            "preferences", "privacy",
            "restaurant", "date_joined", "created_at", "updated_at", "is_active"
        ]
        read_only_fields = ["id", "wallet_balance", "loyalty_points", "date_joined", "created_at", "updated_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id", "name", "email", "password", "role", "phone", "address",
            "restaurant", "preferences", "privacy"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
        
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        refresh = RefreshToken.for_user(user)
        attrs['access'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)
        attrs['id'] = user.id
        attrs['name'] = user.name
        attrs['email'] = user.email
        attrs['phone'] = user.phone
        attrs['address'] = user.address
        attrs['role'] = user.role
        attrs['wallet_balance'] = user.wallet_balance
        attrs['loyalty_points'] = user.loyalty_points
        attrs['created_at'] = user.created_at

        return attrs