# Generated by Django 5.0.7 on 2025-02-05 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_usercontribution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercontribution',
            name='total_likes',
        ),
        migrations.RemoveField(
            model_name='usercontribution',
            name='total_self_comments',
        ),
    ]
