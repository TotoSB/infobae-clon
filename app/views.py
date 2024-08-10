from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import *
from .forms import RegisterForm, LoginForm, PostsForm
from datetime import datetime
from django.http import HttpResponse


today = datetime.now()
formatted_date = today.strftime("%d %b, %Y").replace('Jan', 'Ene').replace('Feb', 'Feb').replace('Mar', 'Mar').replace('Apr', 'Abr').replace('May', 'May').replace('Jun', 'Jun').replace('Jul', 'Jul').replace('Aug', 'Ago').replace('Sep', 'Sep').replace('Oct', 'Oct').replace('Nov', 'Nov').replace('Dec', 'Dic')
themes = mainThemes.objects.all()

context = {
        "themes": themes,
        'today': formatted_date
}

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
        theme_get = mainThemes.objects.get(name=theme_name)
        #Enviamos todos los temas luego de la validacion
        themes = mainThemes.objects.all()
        # Filtramos los posts que tienen ese tema
        news = Posts.objects.filter(main_theme=theme_get)

        context['posts'] = news

        return render(request, "theme.html", context)
    except mainThemes.DoesNotExist:
        return redirect('index')
    
def profile(request, name_autor):
    try:
        profile_get = CustomUser.objects.get(nombre=name_autor)
        context['user_get'] = profile_get
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
    context['form'] = form
    return render(request, 'login.html', context)


def unlogin(request):
    logout(request)
    return redirect('index')

def create_post(request):
    user = request.user

    if user.is_staff:
        # Define `form` antes de la condición POST
        form = PostsForm()

        if request.method == 'POST':
            form = PostsForm(request.POST, request.FILES)
            if form.is_valid():
                postt = form.save(commit=False)
                postt.author = request.user
                postt.save()
                return redirect('index')
        
        return render(request, 'panel/create_post.html', {'form': form})
    else:
        return redirect('index')

def view_post(request, theme_name, pk):
    post_get = get_object_or_404(Posts, id=pk)
    if post_get.main_theme.name == theme_name:
        post_get.reads =+ 1
        context['post_get'] = post_get
        post_get.save()


        return render(request, 'post.html', context)
    else:
        return redirect('index')