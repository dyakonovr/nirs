from django.db import models
from apps.articles.models import Topic

class Dictionary(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.Model)
    term = models.TextField()
    definition = models.TextField()
