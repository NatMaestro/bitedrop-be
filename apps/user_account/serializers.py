from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                attrs["user"] = user
                return attrs
            else:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include email and password.")

    # Include user data in response
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True, allow_blank=True)
    address = serializers.CharField(read_only=True, allow_blank=True)
    restaurant = serializers.CharField(source="restaurant.id", read_only=True, allow_null=True)
    wallet_balance = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    loyalty_points = serializers.IntegerField(read_only=True)
    must_change_password = serializers.BooleanField(read_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "password_confirm", "phone", "address"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "role",
            "password",
            "phone",
            "address",
            "restaurant",
            "wallet_balance",
            "loyalty_points",
            "must_change_password",
            "is_active",
            "date_joined",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "wallet_balance",
            "loyalty_points",
            "date_joined",
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "role",
            "phone",
            "address",
            "restaurant",
            "wallet_balance",
            "loyalty_points",
            "must_change_password",
            "is_active",
            "date_joined",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "wallet_balance",
            "loyalty_points",
            "date_joined",
            "created_at",
            "updated_at",
        ]


class UserListSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    restaurant = serializers.CharField(source="restaurant.id", read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "role",
            "phone",
            "restaurant",
            "restaurant_name",
            "must_change_password",
            "is_active",
            "date_joined",
        ]


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for forced password change on first login.
    """
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')

        if new_password != new_password_confirm:
            raise serializers.ValidationError("New passwords don't match.")

        return attrs


class StaffCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            "email",
            "name",
            "password",
            "phone",
        ]

    def create(self, validated_data):
        # Ensure staff role and restaurant assignment
        validated_data["role"] = "staff"
        validated_data["restaurant"] = self.context["request"].user.restaurant
        user = User.objects.create_user(**validated_data)
        return user


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "role",
            "phone",
            "is_active",
            "date_joined",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "role",
            "date_joined",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        # Remove password from validated_data if it exists
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance