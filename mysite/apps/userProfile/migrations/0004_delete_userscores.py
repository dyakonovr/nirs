# Generated by Django 4.1.5 on 2023-03-17 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0003_rename_user_score_1_userscores_user_score_13_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserScores',
        ),
    ]