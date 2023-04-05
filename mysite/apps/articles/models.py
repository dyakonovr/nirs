from django.db import models


class Topic(models.Model):
    topic = models.TextField()

    def __str__(self):
        return self.topic


class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return self.question


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.option


class TopicMaterials(models.Model):
    topic = models.OneToOneField(
        Topic, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField()
    mainPhoto = models.URLField(default='')
    videos = models.URLField(default='')
    presentation = models.TextField()
    photos = models.URLField(default='')
    personInfo = models.TextField(default='')

    def __str__(self):
        return self.topic
