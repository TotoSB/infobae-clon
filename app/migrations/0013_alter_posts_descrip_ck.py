# Generated by Django 5.0.7 on 2024-08-10 03:20

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_posts_descrip_ck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='descrip_ck',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]