from django.db import models
from authentication.models import User
# Create your models here.


class Question(models.Model):
    q_no = models.IntegerField(primary_key=True)
    question = models.TextField(max_length=200)
    opt1 = models.CharField(max_length=100, null=True)
    opt2 = models.CharField(max_length=100, null=True)
    opt3 = models.CharField(max_length=100, null=True)
    opt4 = models.CharField(max_length=100, null=True)
    ans = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(User, related_name='created_user', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=True)


class Answer(models.Model):
    q_no = models.ForeignKey(Question, related_name='question_no', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='user_name', on_delete=models.PROTECT)
    ans = models.CharField(max_length=100, null=True)
    answered_at = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=True)



