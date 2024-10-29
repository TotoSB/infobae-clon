from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Posts, mainThemes, CustomUser, Tags, SavedPost
from .forms import RegisterForm, LoginForm, PostsForm
from django.contrib.auth import login as auth_login
from datetime import datetime
from django.db.models import Count, Sum
from django.contrib import messages

import requests
from django.contrib.auth.decorators import login_required


def get_global_data():
    response_dlls = requests.get("https://dolarapi.com/v1/dolares")
    data_dlls = response_dlls.json()
    themes = mainThemes.objects.annotate(
        num_posts=Count('posts')
    ).order_by('-num_posts')[:5]
    all_themes = mainThemes.objects.all()
    today = datetime.now()
    tags = Tags.objects.annotate(
        total_reads=Sum('posts__reads')
    ).order_by('-total_reads')[:5]
    formatted_date = today.strftime("%d %b, %Y").replace('Jan', 'Ene').replace('Feb', 'Feb').replace('Mar', 'Mar').replace('Apr', 'Abr').replace('May', 'May').replace('Jun', 'Jun').replace('Jul', 'Jul').replace('Aug', 'Ago').replace('Sep', 'Sep').replace('Oct', 'Oct').replace('Nov', 'Nov').replace('Dec', 'Dic')
    return {
        "themes": themes,
        'today': formatted_date,
        "dollars": data_dlls,
        "all_themes": all_themes,
        "pop_tags": tags,
    }

def index(request):
    postings = Posts.objects.filter(featured=False)
    context = get_global_data()
    try:
        post_feat = Posts.objects.get(featured=True)
        context.update({
        "posts": postings,
        "feat": post_feat
        })
    except Posts.DoesNotExist:
        context.update({
        "posts": postings,

    })
    return render(request, "index.html", context)

def theme_view(request, theme_name):
    try:
        theme_get = mainThemes.objects.get(name=theme_name)
        news = Posts.objects.filter(main_theme=theme_get)
        context = get_global_data()
        context.update({
            'posts': news,
            'title_theme': theme_name
        })
        return render(request, "theme.html", context)
    except mainThemes.DoesNotExist:
        return redirect('index')
    

def profile(request, name_autor):
    try:
        profile_get = CustomUser.objects.get(nombre=name_autor)
        posts_profile = Posts.objects.filter(author=profile_get)
        context = get_global_data()
        context.update({
            'user_get': profile_get,
            'posts_user': posts_profile
        })
        return render(request, "profile.html", context)
    except CustomUser.DoesNotExist:
        return redirect('index')

def register(request):
    context = get_global_data()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('index')
    else:
        form = RegisterForm()

    context['form'] = form
    return render(request, 'registro.html', context)

def login(request):
    context = get_global_data()
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
        if request.method == 'POST':
            form = PostsForm(request.POST, request.FILES)
            if form.is_valid():
                postt = form.save(commit=False)
                postt.author = request.user

                new_main_theme = form.cleaned_data.get('new_main_theme')
                if new_main_theme:
                    main_theme_obj, created = mainThemes.objects.get_or_create(name=new_main_theme)
                    postt.main_theme = main_theme_obj
                else:
                    postt.main_theme = form.cleaned_data.get('main_theme')

                postt.save()

                # Guardar las relaciones ManyToMany
                form.save_m2m()

                return redirect('index')
            else:
                print(form.errors)  # Imprime los errores para depuración
        else:
            form = PostsForm()
        context = get_global_data()
        context['form'] = form
        return render(request, 'panel/create_post.html', context)
    else:
        return redirect('index')

def view_post(request, theme_name, pk):
    post_get = get_object_or_404(Posts, id=pk)
    is_saved = False

    if post_get.main_theme.name == theme_name:
        post_get.reads += 1
        context = get_global_data()
        if request.user.is_authenticated:
            is_saved = SavedPost.objects.filter(user=request.user, post=post_get).exists()
            context['is_saved'] = is_saved
        context['post_get'] = post_get
        post_get.save()
        return render(request, 'post.html', context)
    else:
        return redirect('index')

def edit_post(request, pk):
    post_get = get_object_or_404(Posts, id=pk)
    if post_get.author == request.user:
        if request.method == "POST":
            form = PostsForm(request.POST, instance=post_get)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = PostsForm(instance=post_get)
        context = get_global_data()
        context['form'] = form
        return render(request, 'panel/edit_post.html', context)
    else:
        return redirect('index')

def delete_post(request, pk):
    post_get = get_object_or_404(Posts, id=pk)
    if post_get.author == request.user:
        post_get.delete()
        return redirect('index')
    else:
        return redirect('index')

def search(request):
    text_input = request.POST.get('q')
    search_results = Posts.objects.filter(title__icontains=text_input)
    context = get_global_data()
    context['search'] = search_results
    context['search_title'] = text_input

    return render(request, 'search.html', context)

def subtheme_view(request, theme_name):
    try:
        theme_get = Tags.objects.get(name=theme_name)
        news = Posts.objects.filter(tags_post=theme_get)
        context = get_global_data()
        context.update({
            'posts': news,
            'title_theme': theme_name
        })
        return render(request, "theme.html", context)
    except Tags.DoesNotExist:
        return redirect('index')
    
@login_required
def save_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    user = request.user

    saved_post, created = SavedPost.objects.get_or_create(user=user, post=post)

    if not created:
        saved_post.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def bookmarks(request):
    usuario = request.user
    context = get_global_data()
    guardados = SavedPost.objects.filter(user=usuario)
    context['guardados'] = guardados

    return render(request, "bookmark.html", context)

def usuarios(request):
    context = get_global_data()
    context.update({
        'usuarios': CustomUser.objects.all
    })
    return render(request, "usuarios.html", context)

def make_staff(request, usuario_id):
    user_get = CustomUser.objects.get(id=usuario_id)
    if user_get.is_staff:
        user_get.is_staff = False
        messages.success(request, f"El usuario {user_get.nombre} ya no es staff.")
    else:
        user_get.is_staff = True
        messages.success(request, f"El usuario {user_get.nombre} ahora es staff.")
    user_get.save()
    return redirect('usuarios')