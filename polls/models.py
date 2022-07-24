import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    class Meta:
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return self.question_text

    def was_published_recently(self) -> bool:
        """Returns whether a question was published within the previous 24 hours"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name="date published")


class Choice(models.Model):
    def __str__(self) -> str:
        return self.choice_text

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
