# Generated by Django 4.1.5 on 2023-04-12 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0013_student_rename_studentsgroup_teachersgroup_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachersgroup',
            name='code',
            field=models.TextField(default='', unique=True),
            preserve_default=False,
        ),
    ]
