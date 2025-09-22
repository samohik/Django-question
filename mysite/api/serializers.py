from django.contrib.auth import authenticate, login
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed



