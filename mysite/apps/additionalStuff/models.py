from django.db import models
from apps.articles.models import Topic

class Dictionary(models.Model):
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    term = models.TextField()
    definition = models.TextField()
    order = models.IntegerField(default=-1)


class Dates(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date = models.TextField()
    description = models.TextField(default =  " — ")