# Generated by Django 5.0.7 on 2025-02-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
