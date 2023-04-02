# Generated by Django 4.1.5 on 2023-03-25 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0008_photos_microtopic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.TextField()),
                ('definition', models.TextField()),
                ('topic', models.ForeignKey(on_delete=models.Model, to='articles.topic')),
            ],
        ),
    ]