# Generated by Django 4.1.5 on 2023-04-08 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userProfile', '0011_rename_studentgroup_studentsgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentsgroup',
            name='group',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='studentsgroup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to=settings.AUTH_USER_MODEL),
        ),
    ]