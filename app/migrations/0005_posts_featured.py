# Generated by Django 5.0.7 on 2024-08-03 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_posts_image_banner_posts_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]