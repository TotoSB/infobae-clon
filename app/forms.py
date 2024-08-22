from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Posts, Tags, mainThemes


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    # Añade cualquier otro campo que necesites

    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'password1', 'password2',)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class PostsForm(forms.ModelForm):
    new_tags = forms.CharField(
        required=False,
        label="Nuevas etiquetas:",
        help_text='Introduce nuevos tags separados por comas.'
    )
    new_main_theme = forms.CharField(
        required=False,
        label="Nuevo tema:",
        help_text='Introduce un nuevo tema principal si no está en la lista.'
    )
    main_theme = forms.ModelChoiceField(
        queryset=mainThemes.objects.all(),
        label="Tema principal:",
        required=False,  # Permite dejarlo en blanco si se introduce un nuevo tema
    )

    class Meta:
        model = Posts
        fields = [
            'title',
            'image_banner',
            'short_description',
            'main_theme',
            'descripcion',
            'tags_post',
            'featured',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'tags_post': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'title': 'Título',
            'image_banner': 'Imagen principal:',
            'short_description': 'Descripción Corta',
            'main_theme': 'Tema Principal',
            'descripcion': 'Descripción General',
            'tags_post': 'SubTemas',
            'featured': 'Destacado',
        }

    def clean(self):
        cleaned_data = super().clean()
        new_tags = cleaned_data.get('new_tags', '')
        new_main_theme = cleaned_data.get('new_main_theme', '')

        # Manejo de nuevos tags
        if new_tags:
            tags = [tag.strip() for tag in new_tags.split(',')]
            created_tags = []
            for tag in tags:
                tag_obj, created = Tags.objects.get_or_create(name=tag)
                created_tags.append(tag_obj)
            cleaned_data['tags_post'] = created_tags

        return cleaned_data