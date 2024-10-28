from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import os
from PIL import Image

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  # Utiliza set_password para encriptar la contraseña
        else:
            user.set_password(self.make_random_password())  # Genera una contraseña aleatoria si no se proporciona una
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=650)
    logo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True, default='default.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['nombre']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.logo.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.logo.path)
    

class mainThemes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image_banner = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    short_description = models.CharField(max_length=400)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    main_theme = models.ForeignKey(mainThemes, on_delete=models.DO_NOTHING, null=True)
    tags_post = models.ManyToManyField(Tags, blank=True)
    featured = models.BooleanField(default=False)
    reads = models.IntegerField(default=0)
    descripcion = RichTextUploadingField()


    def save(self, *args, **kwargs):
        if self.featured:
            Posts.objects.exclude(id=self.id).update(featured=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'Vistas: {self.reads} Autor: {self.author.nombre}, Titulo: {self.title}'

class SavedPost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
