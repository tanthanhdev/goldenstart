from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.utils import timezone
from django.db import transaction
import uuid
import time
from django.utils.text import slugify 
from django.utils.crypto import get_random_string
from django.core.validators import validate_image_file_extension
from django.db.models.signals import post_save
from django.dispatch import receiver

from .manager import CustomUserManager
# Create your models here.

def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=4)
    return unique_slug


# extend User system table
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=150)
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(blank=True, max_length=30)
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.\
                                              Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    mail_submitted_at = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email

def document_upload_file(instance, filename):
    timestamp = str(int(time.time()))
    return "documents/{user}/{type}/{filename}".format(
        user=instance.user.email, 
        type=instance.type , 
        filename=f"Additive_{timestamp}_{filename}"
    )

class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ("PDF", "pdf"),
        ("EXCEL", "excel"),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_documents")
    type = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES)
    document = models.FileField(upload_to=document_upload_file)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def email(self):
        return self.user.email 
    
class Tracking(models.Model):
    visits = models.BigIntegerField(default=0)
    download_count = models.BigIntegerField(default=0)