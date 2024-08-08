from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Themes)
admin.site.register(mainThemes)
admin.site.register(Posts)
admin.site.register(ImagesPosts)