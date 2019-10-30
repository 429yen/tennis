# Generated by Django 2.1.7 on 2019-10-12 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20191011_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='good',
            name='whose',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='good_whose', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, default=1, to=settings.AUTH_USER_MODEL),
        ),
    ]
