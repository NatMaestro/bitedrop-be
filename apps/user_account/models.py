from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# ===============================
# Custom User Manager
# ===============================
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, name, password, **extra_fields)


# ===============================
# Custom User Model
# ===============================
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
        ("restaurant_admin", "Restaurant Admin"),
        ("staff", "Restaurant Staff"),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Restaurant relationship (if user is admin or staff)
    restaurant = models.ForeignKey(
        "restaurant.Restaurant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    loyalty_points = models.IntegerField(default=0)

    preferences = models.JSONField(default=dict, blank=True)
    privacy = models.JSONField(default=dict, blank=True)

    # System fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser
