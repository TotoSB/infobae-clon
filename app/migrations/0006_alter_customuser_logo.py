# Generated by Django 5.0.7 on 2024-08-03 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_posts_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/'),
        ),
    ]
