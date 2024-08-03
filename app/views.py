from django.shortcuts import render, redirect
from .models import *
from datetime import datetime

# Create your views here.
def index(request):
    postings = Posts.objects.all()
    themes = Themes.objects.all()
    today = datetime.now()
    formatted_date = today.strftime("%d %b, %Y").replace('Jan', 'Ene').replace('Feb', 'Feb').replace('Mar', 'Mar').replace('Apr', 'Abr').replace('May', 'May').replace('Jun', 'Jun').replace('Jul', 'Jul').replace('Aug', 'Ago').replace('Sep', 'Sep').replace('Oct', 'Oct').replace('Nov', 'Nov').replace('Dec', 'Dic')

    # images_first = ImagesPosts.objects.get(order=1)
    context = {
        "posts": postings,
        "themes": themes,
        'today': formatted_date
    }

    return render(request, "index.html", context)

def theme_view(request, theme_name):
    try:
        # Comprobamos si existe el tema recibido
        theme_get = Themes.objects.get(name=theme_name)
        #Enviamos todos los temas luego de la validacion
        themes = Themes.objects.all()
        # Filtramos los posts que tienen ese tema
        news = Posts.objects.filter(theme=theme_get)
        today = datetime.now()
        formatted_date = today.strftime("%d %b, %Y").replace('Jan', 'Ene').replace('Feb', 'Feb').replace('Mar', 'Mar').replace('Apr', 'Abr').replace('May', 'May').replace('Jun', 'Jun').replace('Jul', 'Jul').replace('Aug', 'Ago').replace('Sep', 'Sep').replace('Oct', 'Oct').replace('Nov', 'Nov').replace('Dec', 'Dic')

        context = {
            'posts': news,
            'themes': themes,
            'today': formatted_date
        }

        return render(request, "theme.html", context)
    except Themes.DoesNotExist:
        return redirect('index')
    
def profile(request, name_autor):
    try:
        profile_get = CustomUser.objects.get(nombre=name_autor)
        today = datetime.now()
        formatted_date = today.strftime("%d %b, %Y").replace('Jan', 'Ene').replace('Feb', 'Feb').replace('Mar', 'Mar').replace('Apr', 'Abr').replace('May', 'May').replace('Jun', 'Jun').replace('Jul', 'Jul').replace('Aug', 'Ago').replace('Sep', 'Sep').replace('Oct', 'Oct').replace('Nov', 'Nov').replace('Dec', 'Dic')


        context = {
            "user_get": profile_get,
            'today': formatted_date
        }
        return render(request, "profile.html", context)
    except CustomUser.DoesNotExist:
        return redirect('index')