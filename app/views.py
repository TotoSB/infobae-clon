from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    postings = Posts.objects.all()
    themes = Themes.objects.all()
    # images_first = ImagesPosts.objects.get(order=1)

    return render(request, "index.html", {"posts": postings, "themes": themes})

def theme(request, theme):
    try:
        theme_get = Themes.objects.get(name=theme)
        return render(request, "theme.html")
    except: 
        return redirect('index')