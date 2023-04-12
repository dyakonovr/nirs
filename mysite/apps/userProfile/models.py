from django.db import models
from apps.authentication.models import User


class UserScores(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    user_score_11 = models.IntegerField(default=0)
    user_score_12 = models.IntegerField(default=0)
    user_score_13 = models.IntegerField(default=0)
    user_score_14 = models.IntegerField(default=0)
    user_score_15 = models.IntegerField(default=0)
    user_score_16 = models.IntegerField(default=0)
    user_score_17 = models.IntegerField(default=0)
    user_score_18 = models.IntegerField(default=0)
    user_score_19 = models.IntegerField(default=0)
    user_score_20 = models.IntegerField(default=0)
    user_score_21 = models.IntegerField(default=0)
    user_score_22 = models.IntegerField(default=0)
    user_score_23 = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class TeachersGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group')
    group = models.CharField(max_length=255)
    code = models.TextField()
    def __str__(self):
        return self.group
    
class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(TeachersGroup,on_delete=models.CASCADE)