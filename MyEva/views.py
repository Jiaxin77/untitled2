from django.shortcuts import render,redirect,reverse,render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from MyEva.models import UserList
from MyEva.models import MethodList
from MyEva.models import IndexList
from MyEva.models import SurveyList
from MyEva.models import AssessList
from MyEva.models import QuestionList
from MyEva.models import ChoiceList
from MyEva.models import ScaleList
from MyEva.models import PaperList
from MyEva.models import AnswerList
from MyEva.models import FIBAnswerList
from MyEva.models import SCAList
from MyEva.models import MCAList
from MyEva.models import ScaleAnswerList

from django.contrib import  messages
import os
import json
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
                    #return render(request, "chooseEva.html", {"user": username})
                    return HttpResponseRedirect(reverse('chooseEva'))
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
            thisAssess=AssessList.objects.get(AssessName=EvaName,AssessOneDes=EvaDetail,AssessType=0, AssessUseNum=EvaUseNum,UserId=USER)
            #thisAssessId=thisAssess.AssessId
            SurveyList.objects.create(AssessId=thisAssess,SurveyName=EvaName,SurveyUseNum=EvaUseNum)
            global ThisQNaire
            ThisQNaire=SurveyList.objects.get(AssessId=thisAssess,SurveyName=EvaName)
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


#	var Question=[ { "id": 1, "title": "丁程鑫帅不帅", "type": "SingleChoose", "ChooseA": "超帅", "ChooseB": "特别帅", "ChooseC": "帅炸了", "ChooseD": "巨帅" }, { "id": 2, "title": "李汶翰能不能出道", "type": "MultiChoose", "ChooseA": "C位出道", "ChooseB": "必须top", "ChooseC": "一位必须的", "ChooseD": "当然可以" }, { "id": 3, "title": "嘻嘻嘻嘻", "type": "Paragraph" }, { "id": 4, "title": "爱不爱我", "type": "Scale", "lowest": "不爱", "highest": "爱", "ScaleCount": 5 }, { "id": 5, "title": "你猜我是谁", "type": "FillInBlank" } ];

#录入数据——得到问卷
def getFillAssess(request):
    #assessId = json.loads(request.body)
    assessId=json.loads(request.GET['assess'])
    #先get到assess的id
    Assess=AssessList.objects.get(AssessId=assessId)
    if Assess.AssessType == 0:
        HtmlQuestionsList=[]
        Survey=SurveyList.objects.get(AssessId=Assess.AssessId)
        Questions=QuestionList.objects.filter(SurveyId=Survey)
        print(type(Questions))
        for que in Questions:
            j=1
            if que.QuestionType == 1:
                tempQue={'id':j,'queId':'','title':'title','type':'SingleChoose','ChooseA':'','ChooseB':'','ChooseC':'','ChooseD':'',"answer":''}
                tempQue['queId']=que.QuestionId
                tempQue['title']=que.QueDescription
                choices=ChoiceList.objects.get(QuestionId=que)
                tempQue['ChooseA']=choices.ChoiceA
                tempQue['ChooseB']=choices.ChoiceB
                tempQue['ChooseC']=choices.ChoiceC
                tempQue['ChooseD']=choices.ChoiceD
                HtmlQuestionsList.append(tempQue)
                j=j+1
            elif que.QuestionType == 2:
                tempQue={'id':j,'queId':'','title':'title','type':'MultiChoose','ChooseA':'','ChooseB':'','ChooseC':'','ChooseD':'','answer':[]}
                tempQue['queId']=que.QuestionId
                tempQue['title']=que.QueDescription
                choices=ChoiceList.objects.get(QuestionId=que)
                tempQue['ChooseA']=choices.ChoiceA
                tempQue['ChooseB']=choices.ChoiceB
                tempQue['ChooseC']=choices.ChoiceC
                tempQue['ChooseD']=choices.ChoiceD
                HtmlQuestionsList.append(tempQue)
                j=j+1
            elif que.QuestionType == 3:
                tempQue={ 'id':j,'queId':'','title':'title','type': 'FillInBlank','answer':''}
                tempQue['queId']=que.QuestionId
                tempQue['title']=que.QueDescription
                HtmlQuestionsList.append(tempQue)
                j=j+1
            elif que.QuestionType == 4:
                tempQue={'id':j,'queId':'','title':'title','type':'Scale','lowest': 'lowest','highest':'highest', 'ScaleCount': 0 ,'answer':''}
                tempQue['queId']=que.QuestionId
                tempQue['title']=que.QueDescription
                scale=ScaleList.objects.get(QuestionId=que)
                tempQue['lowest']=scale.BeginIndex
                tempQue['highest']=scale.EndIndex
                tempQue['ScaleCount']=scale.DegreeNum
                HtmlQuestionsList.append(tempQue)
                j=j+1
            elif que.QuestionType == 5:
                #"id": 3, "title": "嘻嘻嘻嘻", "type": "Paragraph"
                tempQue={'id':j,'queId':'','title':'title','type':'Paragraph'}
                tempQue['queId']=que.QuestionId
                tempQue['title']=que.QueDescription
                HtmlQuestionsList.append(tempQue)
                j=j+1
        print(HtmlQuestionsList)
        return render(request,"FillQNaire.html",{'QuestionList':json.dumps(HtmlQuestionsList),'SurveyId':Survey.SurveyId})
    else:
        return render(request,"chooseEva.html")
    #判断类型 如果是问卷
    #从问卷列表中查询此assessid 得到问卷id
    #从问题列表中查询此问卷id的所有问题
    #逐个问题判断类型，完善成数据格式，传回

def FillQNaire(request):
    Messages=json.loads(request.body)
    Answers=Messages['AllQuestions']
    thisSurveyId=Messages['Survey']
    global USER
    print(USER.UserName)
    thisSurvey=SurveyList.objects.get(SurveyId=thisSurveyId)
    thisPaper = PaperList.objects.filter(UserId=USER, SurveyId=thisSurvey)
    if  thisPaper.exists():
        print("您已填过该问卷！不可重复填写！")
        messages.error(request,"您已填过该问卷！不可重复填写！")
        return render(request,"FillQNaire.html")
    else:
        #增加一个填问卷的人
        surveyedNum=thisSurvey.SurveyUseNum * thisSurvey.SurveyPro
        print(surveyedNum)
        surveyedNum=surveyedNum+1
        print(surveyedNum)
        pro=surveyedNum*100/thisSurvey.SurveyUseNum
        print(pro)
        thisSurvey.SurveyPro=pro
        thisSurvey.save()
        assessId=thisSurvey.AssessId

        PaperList.objects.create(UserId=USER,SurveyId=thisSurvey)
        thisPaper=PaperList.objects.get(UserId=USER,SurveyId=thisSurvey)
        for ans in Answers:
            print(type(ans))
            print(ans['queId'])
            if ans['type']=='SingleChoose':#单选题
                thisQuestion=QuestionList.objects.get(QuestionId=ans['queId'])
                AnswerList.objects.create(QuestionType=1, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                thisAnswer = AnswerList.objects.get(QuestionType=1, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                SCAList.objects.create(ChoiceAnswer=ans['answer'],AnswerId=thisAnswer)
            elif ans['type']=='MultiChoose':#多选题
                AnswerList.objects.create(QuestionType=2, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                thisAnswer = AnswerList.objects.get(QuestionType=2, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                MCAanswers=','.join(ans['answer'])
                MCAList.objects.create(ChoiceAnswer=MCAanswers,ChoiceNum=len(ans['answer']),AnswerId=thisAnswer)
            elif ans['type']=='FillInBlank':#填空题
                AnswerList.objects.create(QuestionType=3, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                thisAnswer = AnswerList.objects.get(QuestionType=3, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                FIBAnswerList.objects.create(FIBAnswer=ans['answer'],AnswerId=thisAnswer)
            elif ans['type']=='Scale':#量表题
                AnswerList.objects.create(QuestionType=4, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                thisAnswer = AnswerList.objects.get(QuestionType=4, isMust=1, PaperId=thisPaper,QuestionId=thisQuestion)
                ScaleAnswerList.objects.create(DegreeAnswer=ans['answer'],AnswerId=thisAnswer)
            elif ans['type']=='Paragraph':
                print("段落")

        messages.success(request,"成功提交！")
        return render(request,"chooseEva.html")
    return render(request, "chooseEva.html")


    #有问卷id
    #录入答卷列表
    #问卷和assess的process要增加

#def deleteAssess(request):
    #get assessid
    #删除对应assessid
    #回到chooseEva 的url？

#def AnalysisData(request):
    #获取问卷id
    #获取问卷所有问题
    #对应问题类型if
    #根据问题id找答卷答案 统计