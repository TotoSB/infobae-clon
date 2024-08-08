from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=650)
    logo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True)
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
    

class Themes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    image_banner = models.ImageField(upload_to="posts/%Y/%m/%d/")
    short_description = models.CharField(max_length=400)
    description = models.CharField(max_length=100000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    theme = models.ManyToManyField(Themes)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f'Autor: {self.author.nombre}, Titulo: {self.title}'

class ImagesPosts(models.Model):
    content = models.ImageField(upload_to="posts/%Y/%m/%d/")
    order = models.IntegerField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)