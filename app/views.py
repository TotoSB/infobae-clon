from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import *
from .forms import RegisterForm, LoginForm
from datetime import datetime
today = datetime.now()
formatted_date = today.strftime("%d %b, %Y").replace('Jan', 'Ene').replace('Feb', 'Feb').replace('Mar', 'Mar').replace('Apr', 'Abr').replace('May', 'May').replace('Jun', 'Jun').replace('Jul', 'Jul').replace('Aug', 'Ago').replace('Sep', 'Sep').replace('Oct', 'Oct').replace('Nov', 'Nov').replace('Dec', 'Dic')
themes = Themes.objects.all()

# Create your views here.
def index(request):
    postings = Posts.objects.all()

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

        context = {
            "user_get": profile_get,
            'today': formatted_date
        }
        return render(request, "profile.html", context)
    except CustomUser.DoesNotExist:
        return redirect('index')
    
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Puedes redirigir a donde quieras después del registro exitoso
            return redirect('index')
    else:
        form = RegisterForm()
    context = {
        "themes": themes,
        'today': formatted_date
    }
    context['form'] = form
    return render(request, 'registro.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    context = {
        "themes": themes,
        'today': formatted_date
    }
    context['form'] = form
    return render(request, 'login.html', context)


def unlogin(request):
    logout(request)
    return redirect('index')
