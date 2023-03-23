from django.contrib import admin
from . models import Topic, Question, TopicMaterials, QuestionOption

admin.site.register(Topic)
admin.site.register(TopicMaterials)
admin.site.register(Question)
admin.site.register(QuestionOption)
