# Generated by Django 4.1.5 on 2023-04-12 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0014_teachersgroup_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachersgroup',
            name='code',
            field=models.TextField(),
        ),
    ]