# Generated by Django 5.0.7 on 2024-08-12 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_customuser_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='tags_post',
            field=models.ManyToManyField(blank=True, to='app.tags'),
        ),
    ]
