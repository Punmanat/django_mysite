from django.db import models

# Create your models here.
# models database auto gen by django
class Poll(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    del_flag = models.BooleanField(default=False)


class Question(models.Model):
    text = models.TextField()
    single = '01'
    multiple = '02'
    TYPES = (
        (single, 'Single answer'),
        (multiple, 'Multiple answer')
    )

    type = models.CharField(max_length=2, choices=TYPES, default='01')
    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)


class Choice(models.Model):
    text = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

class Answer(models.Model):
    choice = models.OneToOneField(Choice, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
