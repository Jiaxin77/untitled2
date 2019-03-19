from django.shortcuts import render
from django.http import HttpResponse
from MyEva.models import UserList
from MyEva.models import MethodList
from MyEva.models import IndexList
from MyEva.models import SurveyList
from MyEva.models import AssessList
from MyEva.models import QuestionList
from MyEva.models import ChoiceList
from MyEva.models import ScaleList
from django.contrib import  messages

import json
# Create your views here.





def index(request):
      return render(request, "login.html", {"message": ""})

def login(request):
    result = ""
    global USER
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        thisUser = UserList.objects.filter(UserName=username)
        print(type(thisUser))
        print(thisUser)
        #判断是否为空
        if thisUser.exists():
            for user in thisUser:
                if user.Password == password:
                    result = "登录成功"
                    #messages.success(request,"登录成功")
                    USER = user
                    return render(request, "chooseEva.html", {"user": username})
                else:
                    messages.error(request,"密码错误")
                    result = "密码错误"
        else:
            messages.error(request,"用户不存在")
            result = "用户不存在"
    print(result)
    return render(request,"login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("Regusername", None)
        password = request.POST.get("Regpassword", None)
        status = request.POST.get("user_type", None)
        if status == "VIP":
            STANumber = 1
        else:
            STANumber = 0
        if UserList.objects.filter(UserName=username):
            messages.error(request,"用户名已存在")
            return render(request, "login.html")
        else:
            UserList.objects.create(UserName=username, Password=password, Status=STANumber)
            messages.success(request,"注册成功")
    return render(request, "login.html")

# var IndexMessage= [
# 				{
# 					id:1,
# 					title:'易学性',
# 					content:'易学性巴拉巴拉'
# 				},
# 				{
# 					id:2,
# 					title:'容错性',
# 					content:'容错性balabala'
# 				},
# 				{
# 					id:3,
# 					title:'便捷性',
# 					content:'便捷性巴拉巴拉'
# 				}
# 				];


# var MethodMessage=[
# 	{
# 		id:1,
# 		title:'层次分析法',
# 		content:'层次分析法babala'
# 	},
# 	{
# 		id:2,
# 		title:'启发式评估法',
# 		content:'启发式评估法balabala'
# 	},
# 	{
# 		id:3,
# 		title:'可用性测试法',
# 		content:'可用性测试法balabala'
# 	}
# 	];
def indexandmethod(request):
    HtmlIndexList=[]
    HtmlMethodList=[]
    MyIndexList = IndexList.objects.values('FatherName', 'Description').distinct()
    MyMethodList = MethodList.objects.values('MethodName','Description').distinct()
    i=0
    for index in MyIndexList:
        tempIndex={'id':i,'title':'title','content':'content'}
        tempIndex['title']=index['FatherName']
        tempIndex['content']=index['Description'].replace("\n","<br/>")
        i=i+1
        HtmlIndexList.append(tempIndex)
    j=0
    for method in MyMethodList:
        tempMethod={'id':j,'title':'title','content':'content'}
        tempMethod['title']=method['MethodName']
        tempMethod['content']=method['Description'].replace("\n","<br/>")
        j=j+1
        HtmlMethodList.append(tempMethod)
    return render(request, "IndexAndMethod.html",{'IndexList':json.dumps(HtmlIndexList),'MethodList':json.dumps(HtmlMethodList)})

def newEva(request):
    return render(request, "newEva.html")

def newBlankEva(request):
    global USER
    if request.method == "POST":
        EvaType=request.POST.get("eva",None)
        EvaName=request.POST.get("name",None)
        EvaDetail=request.POST.get("detail",None)
        EvaUseNum=request.POST.get("peopleNum",None)

        if EvaType == "survey":
            #新建评估 插入新建的

            AssessList.objects.create(AssessName=EvaName,AssessOneDes=EvaDetail,AssessType=0, AssessUseNum=EvaUseNum,UserId=USER)
            #获取新建的这个id
            thisAssess=AssessList.objects.get(AssessName=EvaName)
            thisAssessId=thisAssess.AssessId
            SurveyList.objects.create(AssessId=thisAssessId,SurveyName=EvaName,SurveyUseNum=EvaUseNum)
            global ThisQNaire
            ThisQNaire=SurveyList.objects.get(AssessId=thisAssessId,SurveyName=EvaName)
            return render(request, "newQNaire.html",{'QNaireName':EvaName})

    return render(request, "newEva.html")

def addQNaire(request):
    print('newQuestions')
    print(request.body)
    obj=json.loads(request.body)
    print(obj)

    if request.method == "POST":
        global ThisQNaire
        Questions=[]
        Questions=obj
        print(type(Questions))
        print(Questions)
        for que in Questions:
            print(que)
            print(que['type'])
            QueDes = que['title']
            if que['type'] == 'SingleChoose':
                queType=1
                QuestionList.objects.create(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
                thisQuestion= QuestionList.objects.get(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
                ChoiceList.objects.create(SCQorMCQ=1,ChoiceA=que['ChooseA'],ChoiceB=que['ChooseB'],ChoiceC=que['ChooseC'],ChoiceD=que['ChooseD'],QuestionId=thisQuestion)
                print("插入成功")
            elif que['type'] == 'MultiChoose':
                queType=2
                QuestionList.objects.create(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
                thisQuestion= QuestionList.objects.get(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
                ChoiceList.objects.create(SCQorMCQ=2,ChoiceA=que['ChooseA'],ChoiceB=que['ChooseB'],ChoiceC=que['ChooseC'],ChoiceD=que['ChooseD'],QuestionId=thisQuestion)
            elif que['type'] == 'FillInBlank':
                queType=3
                QuestionList.objects.create(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
            elif que['type'] == 'Scale':
                queType=4
                QuestionList.objects.create(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
                thisQuestion= QuestionList.objects.get(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)
                ScaleList.objects.create(BeginIndex=que['lowest'],EndIndex=que['highest'],DegreeNum=que['ScaleCount'],QuestionId=thisQuestion)
            elif que['type'] == 'Paragraph':
                queType=5
                QuestionList.objects.create(QueDescription=QueDes,QuestionType=queType,isMust=1,SurveyId=ThisQNaire)

    return render(request, "newEva.html")
#
# var AllAssess=[
# 		{
# 			id:1,
# 			name:"评估名称1",
# 			person:"曲丽丽",
# 			InShort:"我是评估1一句话描述",
# 			BeginTime:"2018-06-16 14:03",
# 			process:90,
# 			condition:"ing"
# 		},
# 		{
# 			id:2,
# 			name:"评估名称2",
# 			person:"丁程鑫",
# 			InShort:"我是评估2一句话描述",
# 			BeginTime:"2018-06-18 17:03",
# 			process:30,
# 			condition:"ing"
# 		},
# 		{
# 			id:3,
# 			name:"评估名称3",
# 			person:"马嘉祺",
# 			InShort:"我是评估3一句话描述",
# 			BeginTime:"2018-03-18 17:03",
# 			process:100,
# 			condition:"End"
# 		},
# 		{
# 			id:4,
# 			name:"评估名称3",
# 			person:"李汶翰",
# 			InShort:"我是评估4一句话描述",
# 			BeginTime:"2017-03-18 17:03",
# 			process:100,
# 			condition:"End"
# 		}
# 	]



def chooseEva(request):
    print("chooseEva")
    evalist=AssessList.objects.all()
    HtmlEvaList=[]
    for eva in evalist:
        tempeva={'id':0,'name':'','person':'','InShort':'','BeginTime':'','process':'','condition':''}
        tempeva['id']=eva.AssessId
        tempeva['name']=eva.AssessName
        global USER
        tempeva['person']=eva.UserId.UserName
        tempeva['InShort']=eva.AssessOneDes
        tempeva['BeginTime']=str(eva.AssessBeginTime)[0:16]
        tempeva['process']=eva.AssessPro
        if eva.AssessPro != 100:
            tempeva['condition']='ing'
        else:
            tempeva['condition']='End'
        HtmlEvaList.append(tempeva)
    return render(request,"chooseEva.html",{'EvaList':json.dumps(HtmlEvaList)})

#录入数据——得到问卷
def getAssess(request):
    #先get到assess的id
    #判断类型 如果是问卷
    #从问卷列表中查询此assessid 得到问卷id
    #从问题列表中查询此问卷id的所有问题
    #逐个问题判断类型，完善成数据格式，传回

def AnswerQNaire(request):
    #有问卷id
    #录入答卷列表
    #问卷和assess的process要增加

def deleteAssess(request):
    #get assessid
    #删除对应assessid
    #回到chooseEva 的url？

def AnalysisData(request):
    #获取问卷id
    #获取问卷所有问题
    #对应问题类型if
    #根据问题id找答卷答案 统计