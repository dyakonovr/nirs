# Generated by Django 4.1.5 on 2023-03-25 22:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_photos_microtopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='microTopic',
        ),
    ]
