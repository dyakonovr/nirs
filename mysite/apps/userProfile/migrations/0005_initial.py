# Generated by Django 4.1.5 on 2023-03-17 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('userProfile', '0004_delete_userscores'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserScores',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('user_score_11', models.IntegerField(default=0)),
                ('user_score_12', models.IntegerField(default=0)),
                ('user_score_13', models.IntegerField(default=0)),
                ('user_score_14', models.IntegerField(default=0)),
                ('user_score_15', models.IntegerField(default=0)),
                ('user_score_16', models.IntegerField(default=0)),
                ('user_score_17', models.IntegerField(default=0)),
                ('user_score_18', models.IntegerField(default=0)),
                ('user_score_19', models.IntegerField(default=0)),
                ('user_score_20', models.IntegerField(default=0)),
                ('user_score_21', models.IntegerField(default=0)),
                ('user_score_22', models.IntegerField(default=0)),
            ],
        ),
    ]
