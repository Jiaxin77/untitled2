from django.db import models

# Create your models here.
#not null是默认的
class UserList(models.Model):
    UserId = models.CharField(max_length=50,primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Status = models.IntegerField(default=0)

class SurveyList(models.Model):
    SurveyId = models.CharField(max_length=50,primary_key=True)
    AssessId = models.CharField(max_length=50)
    SurveyName = models.CharField(max_length=50)
    SurveyPro = models.IntegerField(default=0)
    SurveyQueNum = models.IntegerField(default=0,null=True)

class QuestionList(models.Model):
    QuestionId = models.CharField(max_length=50,primary_key=True)
    QueDescription = models.CharField(max_length=500,null=True)
    QuestionType = models.IntegerField(default=0)
    isMust = models.BooleanField(blank=True)
    SurveyId = models.CharField(max_length=50)

class ChoiceList(models.Model):
    QuestionId = models.ForeignKey(QuestionList)
    SCQorMCQ = models.IntegerField(default=0)
    ChoiceA = models.CharField(max_length=50)
    ChoiceB = models.CharField(max_length=50)
    ChoiceC = models.CharField(max_length=50)
    ChoiceD = models.CharField(max_length=50)

class ScaleList(models.Model):
    QuestionId = models.ForeignKey(QuestionList)
    BeginIndex = models.CharField(max_length=50)
    EndIndex = models.CharField(max_length=50)
    DegreeNum = models.IntegerField(default=0)

class PaperList(models.Model):



