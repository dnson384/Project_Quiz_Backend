from django.db import models
import uuid


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        TEACHER = "TEACHER", "teacher"
        STUDENT = "STUDENT", "student"

    class LoginMethod(models.TextChoices):
        EMAIL = "EMAIL", "email"
        GOOGLE = "GOOGLE", "google"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.CharField(max_length=20, choices=Role.choices, null=False, blank=False)
    login_method = models.CharField(
        max_length=20, choices=LoginMethod.choices, null=False, blank=False
    )
    avatar_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.user_id)


class UserEmail(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        to_field="user_id",
        primary_key=True,
    )
    password_hashed = models.TextField(null=False, blank=False)

    class Meta:
        db_table = "users_email"

    def __str__(self):
        return str(self.user.user_id)
