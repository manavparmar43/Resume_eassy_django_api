from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import date
import uuid

# Create your models here.


class DateTimeMixin(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        auto_created=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Role(DateTimeMixin):
    name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    name = models.CharField(max_length=250)

    def __str__(self):
        return "{}".format(self.username)


class NonBuiltInUserToken(Token):
    user = models.ForeignKey(
        User,
        related_name="auth_token",
        on_delete=models.CASCADE,
    )
