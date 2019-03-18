from django.db import models
# -- coding: utf-8 --
# Create your models here.
#not null是默认的

#用户列表
class UserList(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Status = models.IntegerField(default=0)

#问卷列表
class SurveyList(models.Model):
    SurveyId = models.AutoField(primary_key=True)
    AssessId = models.CharField(max_length=50)
    SurveyName = models.CharField(max_length=50)
    SurveyPro = models.IntegerField(default=0)
    SurveyUseNum = models.IntegerField(default=0)
    SurveyQueNum = models.IntegerField(default=0,null=True)

#问题列表
class QuestionList(models.Model):
    QuestionId = models.AutoField(primary_key=True)
    QueDescription = models.CharField(max_length=500,null=True)
    QuestionType = models.IntegerField(default=0)
    isMust = models.BooleanField(blank=True)
    SurveyId = models.ForeignKey('SurveyList',on_delete=models.CASCADE)

#选择题列表
class ChoiceList(models.Model):
    QuestionId = models.ForeignKey('QuestionList',on_delete=models.CASCADE)
    SCQorMCQ = models.IntegerField(default=0)
    ChoiceA = models.CharField(max_length=50)
    ChoiceB = models.CharField(max_length=50)
    ChoiceC = models.CharField(max_length=50)
    ChoiceD = models.CharField(max_length=50)

#量表题列表
class ScaleList(models.Model):
    QuestionId = models.ForeignKey('QuestionList',on_delete=models.CASCADE)
    BeginIndex = models.CharField(max_length=50)
    EndIndex = models.CharField(max_length=50)
    DegreeNum = models.IntegerField(default=0)

#答卷列表
class PaperList(models.Model):
    PaperId = models.AutoField(primary_key=True)
    SurveyId = models.CharField(max_length=50)
    UserId = models.CharField(max_length=50)
    UserName = models.CharField(max_length=50)

#答案列表
class AnswerList(models.Model):
    AnswerId = models.AutoField(primary_key=True)
    QuestionType = models.IntegerField(default=0)
    isMust = models.BooleanField(blank=True)
    PaperId = models.ForeignKey('PaperList',on_delete=models.CASCADE)

#单选题答案列表
class SCAList(models.Model):
    AnswerId = models.ForeignKey('AnswerList',on_delete=models.CASCADE)
    QuestionId = models.CharField(max_length=50)
    ChoiceAnswer = models.CharField(max_length=5)

#多选题答案列表
class  MCAList(models.Model):
    AnswerId = models.ForeignKey('AnswerList',on_delete=models.CASCADE)
    QuestionId = models.CharField(max_length=50)
    ChoiceNum = models.IntegerField(default=1)
    ChoiceAnswer = models.CharField(max_length=50)

#填空题答案列表
class FIBAnswerList(models.Model):
    AnswerId = models.ForeignKey('AnswerList',on_delete=models.CASCADE)
    QuestionId = models.CharField(max_length=50)
    FIBAnswer = models.CharField(max_length=100)

#量表题答案列表
class ScaleAnswerList(models.Model):
    AnswerId = models.ForeignKey('AnswerList',on_delete=models.CASCADE)
    QuestionId = models.CharField(max_length=50)
    DegreeAnswer = models.IntegerField(default=1)

#指标库
class IndexList(models.Model):
    IndexId = models.AutoField(primary_key=True)
    IndexName = models.CharField(max_length=50)
    FatherName = models.CharField(max_length=50)
    FamilyName = models.CharField(max_length=50)
    Description = models.CharField(max_length=500)

#方法库
class MethodList(models.Model):
    MethodId = models.AutoField(primary_key=True)
    MethodName = models.CharField(max_length=50)
    Description = models.CharField(max_length=500)

#模板库
class ModelList(models.Model):
    ModelId = models.AutoField(primary_key=True)
    ModelType = models.IntegerField(default=1)
    AssessId = models.CharField(max_length=50)

#评估列表
class AssessList(models.Model):
    AssessId = models.AutoField(primary_key=True)
    AssessName = models.CharField(max_length=50)
    AssessOneDes = models.CharField(max_length=200)
    UserId = models.ForeignKey('UserList',on_delete=models.CASCADE)
    AssessPro = models.IntegerField(default=0)
    AssessType = models.IntegerField(default=1)
    AssessDes = models.CharField(max_length=500)
    AssessObject = models.CharField(max_length=300)
    AssessIndexNum = models.IntegerField(default=0)
    People = models.CharField(max_length=300)
    AssessIndexId = models.CharField(max_length=1000)

#方案列表
class PlanList(models.Model):
    PlanId = models.AutoField(primary_key=True)
    PlanName = models.CharField(max_length=59)
    PlanDescription = models.CharField(max_length=500)
    PlanTypeId = models.CharField(max_length=50)
    AssessId = models.CharField(max_length=50)

#启发式评估表格
class HeuEvaResult(models.Model):
    HeuEvaId = models.AutoField(primary_key=True)
    PlanId = models.CharField(max_length=50)
    IndexId = models.CharField(max_length=50)
    Interface = models.CharField(max_length=50)
    HeuProblem = models.CharField(max_length=300)
    SeriousDegree = models.IntegerField(default=0)
    Advice = models.CharField(max_length=200,null=True)
    ScreenShot = models.CharField(max_length=300,null=True)
    UserId= models.ForeignKey('UserList',on_delete=models.CASCADE)

#记录绩效表格
class PerformanceRecord(models.Model):
    RecordId = models.AutoField(primary_key=True)
    ErrorRate = models.FloatField(default=0)
    FinishTime = models.FloatField(default=0)
    SuccessRate = models.FloatField(default=0)
    LookingTime = models.FloatField(default=0)
    PlanId = models.ForeignKey('PlanList',on_delete=models.CASCADE)
    UserId = models.ForeignKey('UserList',on_delete=models.CASCADE)






