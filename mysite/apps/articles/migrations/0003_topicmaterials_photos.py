# Generated by Django 4.1.5 on 2023-03-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_rename_questionoptions_questionoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicmaterials',
            name='photos',
            field=models.URLField(default=''),
        ),
    ]
