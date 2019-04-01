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
import math
import numpy
import jieba
from collections import Counter
import sys
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
      return render(request, "results2.html")

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

# var Alldatas=[
# {
# 	id:1,
# 	name:"软件人机界面",
# 	FirstList:
# 	[
# 	{
# 		id:11,
# 		listTitle:"易学性",
# 		selected:[],
# 		SecondList:
# 		[
# 		{
# 			id:111,
# 			listTitle:"一致性",
# 			method:"启发式评估法"
# 		},
# 		{
# 			id:112,
# 			listTitle:"认知负荷",
# 			method:"启发式评估法"
# 		}
# 		]
# 	},
# 	{
# 		id:12,
# 		listTitle:"容错性",
# 		selected:[],
# 		SecondList:
# 		[
# 		{
# 			id:121,
# 			listTitle:"防止犯错",
# 			method:"可用性测试"
# 		},
# 		{
# 			id:122,
# 			listTitle:"纠错",
# 			method:"可用性测试"
# 		}
# 		]
# 	},
# 	{
# 		id:13,
# 		listTitle:"易用性",
# 		selected:[],
# 		SecondList:
# 		[
# 		{
# 			id:131,
# 			listTitle:"灵活性",
# 			method:"可用性测试"
# 		},
# 		{
# 			id:132,
# 			listTitle:"适用性",
# 			method:"可用性测试"
# 		}
# 		]
# 	},
#
# 	]
#
#
#
# },
# {
# 	id:2,
# 	name:"系统任务流程",
# 	FirstList:
# 	[
# 	{
# 		id:21,
# 		listTitle:"有效性",
# 		selected:[],
# 		SecondList:
# 		[
# 		{
# 			id:211,
# 			listTitle:"功能完备性",
# 			method:"启发式评估法"
# 		},
# 		{
# 			id:212,
# 			listTitle:"任务有效性",
# 			method:"启发式评估法"
# 		}
# 		]
# 	},
# 	{
# 		id:22,
# 		listTitle:"效率",
# 		selected:[],
# 		SecondList:
# 		[
# 		{
# 			id:221,
# 			listTitle:"任务操作便捷性",
# 			method:"可用性测试"
# 		},
# 		{
# 			id:222,
# 			listTitle:"流程复杂度",
# 			method:"可用性测试"
# 		}
# 		]
# 	}
# 	]
# }
# ];

def getIndexInfo():
    IndexInfo=[]
    AllIndexFamilyName=IndexList.objects.all().values('FamilyName').distinct()
    j=1
    for familyname in AllIndexFamilyName:

        thisFamily=familyname['FamilyName']
        thisFamilyMembers=IndexList.objects.filter(FamilyName=thisFamily)
        tempFamily = {'id': j, 'name':thisFamily,'FirstList':[]}
        Fathers=[]
        #统计FatherName
        for member in thisFamilyMembers:#这个家族的成员
            FatherName=member.FatherName
            Fathers.append(FatherName)
        Fathers = set(Fathers)#去重
        k=1
        for father in Fathers:
            tempFather={'id':j*10+k,'listTitle':father,'selected':[],'SecondList':[]}
            l=1
            for member in thisFamilyMembers:
                if member.FatherName==father:
                    tempIndex={'id':j*100+k*10+l,'listTitle':member.IndexName,'method':member.thisMethod}
                    tempFather['SecondList'].append(tempIndex)
                    l=l+1
            tempFamily['FirstList'].append(tempFather)
            k=k+1
        IndexInfo.append(tempFamily)
        j=j+1
    return IndexInfo

        


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
        elif EvaType == "comprehensive":#新建综合评估
            AssessList.objects.create(AssessName=EvaName,AssessOneDes=EvaDetail,AssessType=1,AssessUseNum=EvaUseNum,UserId=USER)
            thisAssess=AssessList.objects.get(AssessName=EvaName,AssessOneDes=EvaDetail,AssessType=1,AssessUseNum=EvaUseNum,UserId=USER)
            #获取指标信息
            IndexInfo=[]
            IndexInfo=getIndexInfo()
            print(IndexInfo)
            Assess={'AssessId':thisAssess.AssessId,'AssessName':thisAssess.AssessName}
            return  render(request,"edit1.html",{'Assess':Assess,'IndexInfo':IndexInfo})
    return render(request, "newEva.html")





def getEvaInfo(request):
    global ASSESS
    global INDEXS
    INDEXS=[]
    print(request.body)
    Messages = json.loads(request.body)
    ASSESS = request.POST.get("Assess", None)
    INDEXS = Messages['Indexs']#复杂嵌套数据用request.body
    methods = MethodList.objects.all()
    print(INDEXS)
    return  render(request,"editEva2.html",{'Assess':ASSESS,'Index':INDEXS,'Method':methods})


def showEvaInfo(request):
    global INDEXS #正规来讲，index也应该在上个函数中存入数据库，再从数据库中读出
    assessid = json.loads(request.GET['assess'])
    thisAssess=AssessList.objects.get(AssessId=assessid)
    myAssess={'AssessId':assessid,'AssessName':thisAssess.AssessName}
    methods = MethodList.objects.all()
    htmlMethods=[]
    for method in methods:
        temp={'MethodId':method.MethodId,'MethodName':method.MethodName,'dataSource':method.dataSource,'dealData':method.dealData,'people':method.people}
        htmlMethods.append(temp)
    print(INDEXS)
    return  render(request,"editEva2.html",{'Assess':myAssess,'Index':INDEXS,'Method':htmlMethods})


'''
def getEvaPlan(request):
    assess = json.loads(request.GET['Assess'])
    indexs = json.loads(request.GET['Indexs'])
    for family in indexs:
        fathers=[]
        fathers=family.FirstList
        for father in fathers:
            selected=[]
            selected=father.selected
            for index in selected:
                indexName=index.listTitle
                indexMethod=index.method
                methods=indexMethod.split(",")
                for method in methods:
                    if(method == "")
'''



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
        if eva.AssessPro < 100:
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
        surveyedNum=math.ceil((thisSurvey.SurveyUseNum * thisSurvey.SurveyPro)/100)
        print(surveyedNum)
        surveyedNum=surveyedNum+1
        print(surveyedNum)
        pro=surveyedNum*100/thisSurvey.SurveyUseNum
        print(pro)
        if(pro>100):
            pro=100
        thisSurvey.SurveyPro=pro
        thisSurvey.save()
        assessId=thisSurvey.AssessId
        assessedNum=math.ceil((assessId.AssessUseNum*assessId.AssessPro)/100)#向上取整
        assessedNum=assessedNum+1
        assessPro=assessedNum*100/assessId.AssessUseNum
        if(assessPro>100):
            assessPro=100
        assessId.AssessPro=assessPro
        assessId.save()

        PaperList.objects.create(UserId=USER,SurveyId=thisSurvey)
        thisPaper=PaperList.objects.get(UserId=USER,SurveyId=thisSurvey)
        for ans in Answers:
            print(type(ans))
            print(ans['queId'])
            thisQuestion = QuestionList.objects.get(QuestionId=ans['queId'])
            if ans['type']=='SingleChoose':#单选题
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
                print(ans['answer'])
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

def deleteAssess(request):
    Messages = json.loads(request.body)
    assessId = Messages['assess']
    AssessList.objects.filter(AssessId=assessId).delete()
    print("删除成功")
    return  render(request,"chooseEva.html")

def countFrequency(answers):
    myTxt = ''.join(answers)
    # myTxt="李汶翰、嘉羿、管栎、胡春杨、陈宥维、夏瀚宇、施展、邓超元、连淮伟李汶翰、姚明明、管栎、何昶希、胡春杨、陈宥维、连淮伟、陈思键、冯俊杰李汶翰、嘉羿、管栎、胡春杨、连淮伟、夏瀚宇、何昶希、姚明明、冯俊杰、李汶翰、嘉羿、管栎、胡春杨、连淮伟、夏瀚宇、何昶希、姚明明、冯俊杰李汶翰、嘉羿、管栎、胡春杨、连淮伟、夏瀚宇、何昶希、姚明明、冯俊杰"
    myTxt_words = [x for x in jieba.cut(myTxt) if len(x) >= 2]
    c = Counter(myTxt_words).most_common(10)
    print(json.dumps(c, ensure_ascii=False))
    htmlFrequency = []
    for oneWord in c:
        temp = {'name': '', 'value': 0}
        temp['name'] = oneWord[0]
        temp['value'] = oneWord[1]
        htmlFrequency.append(temp)
    return htmlFrequency

def analysisQNaire(assess):
    assessId=assess
    thisSurvey=SurveyList.objects.get(AssessId=assessId)
    thisPapers=PaperList.objects.filter(SurveyId=thisSurvey)
    thisQuestions=QuestionList.objects.filter(SurveyId=thisSurvey)
    thisAnswers=[]
    for paper in thisPapers:
        answers=AnswerList.objects.filter(PaperId=paper)
        for ans in answers:
            thisAnswers.append(ans)
    j=1
    HtmlAnswers=[]
    for que in thisQuestions:
        if que.QuestionType == 1:#单选题
            thisSCQ=ChoiceList.objects.get(QuestionId=que)#获取题目
            chooseANum=0
            chooseBNum=0
            chooseCNum=0
            chooseDNum=0
            completePeople=0
            for thisAns in thisAnswers:
                if thisAns.QuestionId==que:#是这道题的答案
                    completePeople=completePeople+1#有效回答人数+1
                    #print(thisAns.AnswerId)
                    #print(thisAns.QuestionId)
                    #print(thisAns.QuestionId.QueDescription)
                    choiced=SCAList.objects.get(AnswerId=thisAns)#获取具体答案
                    if(choiced.ChoiceAnswer=='A'):
                        chooseANum=chooseANum+1
                    elif(choiced.ChoiceAnswer=='B'):
                        chooseBNum=chooseBNum+1
                    elif(choiced.ChoiceAnswer=='C'):
                        chooseCNum=chooseCNum+1
                    elif(choiced.ChoiceAnswer=='D'):
                        chooseDNum=chooseDNum+1
            temp={'Id':j,'queId':que.QuestionId,'queType':'SingleChoose','title':que.QueDescription,'filledPeople':completePeople,'chooseA':thisSCQ.ChoiceA,'chooseB':thisSCQ.ChoiceB,'chooseC':thisSCQ.ChoiceC,'chooseD':thisSCQ.ChoiceD,'results':[chooseANum,chooseBNum,chooseCNum,chooseDNum],'resultRatio':[ chooseANum/completePeople,chooseBNum/completePeople,chooseCNum/completePeople,chooseDNum/completePeople]}
            HtmlAnswers.append(temp)
            j=j+1
        elif que.QuestionType == 2:#多选题
            thisMCQ=ChoiceList.objects.get(QuestionId=que)
            chooseANum=0
            chooseBNum=0
            chooseCNum=0
            chooseDNum=0
            completePeople=0
            for thisAns in thisAnswers:
                if thisAns.QuestionId==que:#是这道题的答案
                    completePeople=completePeople+1#有效回答人数+1
                    choiced=MCAList.objects.get(AnswerId=thisAns)
                    choicedAnswers=choiced.ChoiceAnswer.split(',')
                    for ca in choicedAnswers:
                        if(ca=='A'):
                            chooseANum=chooseANum+1
                        elif(ca=='B'):
                            chooseBNum=chooseBNum+1
                        elif(ca=='C'):
                            chooseCNum=chooseCNum+1
                        elif(ca=='D'):
                            chooseDNum=chooseDNum+1
            temp={'Id':j,'queId':que.QuestionId,'queType':'MultiChoose','title':que.QueDescription,'filledPeople':completePeople,'chooseA':thisMCQ.ChoiceA,'chooseB':thisMCQ.ChoiceB,'chooseC':thisMCQ.ChoiceC,'chooseD':thisMCQ.ChoiceD,'results':[chooseANum,chooseBNum,chooseCNum,chooseDNum],'resultRatio':[chooseANum/completePeople,chooseBNum/completePeople,chooseCNum/completePeople,chooseDNum/completePeople]}
            HtmlAnswers.append(temp)
            j=j+1
        elif que.QuestionType==4:#量表题
            thisScale=ScaleList.objects.get(QuestionId=que)
            chooseNum=[]
            for i in range(0,thisScale.DegreeNum - 1):
                chooseNum.append(0)
            completePeople=0
            for thisAns in thisAnswers:
                if thisAns.QuestionId==que:
                    completePeople=completePeople+1
                    choosed=ScaleAnswerList.objects.get(AnswerId=thisAns)
                    chooseNum[choosed.DegreeAnswer-1]=chooseNum[choosed.DegreeAnswer-1]+1
            chooseRatio=[]
            for i in range(0,thisScale.DegreeNum - 1):
                chooseRatio.append(chooseNum[i]/completePeople)
            degree=[]
            degree=(numpy.arange(1, thisScale.DegreeNum, 1)).tolist()
            temp={'Id':j,'queId':que.QuestionId,'queType':'Scale','title':que.QueDescription,'Begin':thisScale.BeginIndex,'End':thisScale.EndIndex,'filledPeople':completePeople,'ScaleDegree':degree,'results':chooseNum,'resultRatio':chooseRatio}
            HtmlAnswers.append(temp)
            j=j+1
        elif que.QuestionType==3:#填空题
            FIBAnswers=[]
            completePeople=0
            for thisAns in thisAnswers:
                if thisAns.QuestionId==que:#是这道题的答案
                    completePeople=completePeople+1#有效回答人数+1
                    thisFIBAns=FIBAnswerList.objects.get(AnswerId=thisAns)
                    FIBAnswers.append(thisFIBAns.FIBAnswer)
            htmlFrequency=countFrequency(FIBAnswers)
            temp={'Id':j,'queId':que.QuestionId,'queType':'FillInBlank','title':que.QueDescription,'results':FIBAnswers,'WCResults':htmlFrequency}
            HtmlAnswers.append(temp)
            j=j+1


    return HtmlAnswers
#
# {
# 		Id:3,
# 		queId:"45678",
# 		queType:"FillInBlank",
# 		title:"青春有你出道位？",
# 		results:["李汶翰、嘉羿、管栎、胡春杨、陈宥维、夏瀚宇、施展、邓超元、连淮伟","李汶翰、姚明明、管栎、何昶希、胡春杨、陈宥维、连淮伟、陈思键、冯俊杰",
# 		"李汶翰、嘉羿、管栎、胡春杨、连淮伟、夏瀚宇、何昶希、姚明明、冯俊杰","李汶翰、嘉羿、管栎、胡春杨、连淮伟、夏瀚宇、何昶希、姚明明、冯俊杰",
# 		"李汶翰、嘉羿、管栎、胡春杨、连淮伟、夏瀚宇、何昶希、姚明明、冯俊杰"
# 		],
# 		WCResults:
# 		[{name:"李汶翰",value:95},
# 		{name:"嘉羿",value:74},
# 		{name:"管栎",value:79},
# 		{name:"胡春杨",value:87},
# 		{name:"何昶希",value:67},
# 		{name:"连淮伟",value:56},
# 		{name:"姚明明",value:23},
# 		{name:"冯俊杰",value:21},
# 		{name:"施展",value:56},
# 		{name:"姚弛",value:12},
# 		{name:"陈思键",value:10},
# 		{name:"邓超元",value:5}]
# 	}

#
# {
# 		Id:2,
# 		queId:"23456",
# 		queType:"Scale",
# 		title:"爱不爱我？",
# 		filledPeople:100,
# 		ScaleDegree:[1,2,3,4,5,6,7],
# 		results:[10,5,8,12,15,16,34],
# 		resultRatio:[0.1,0.05,0.08,0.12,0.15,0.16,0.34]
#
# 	}

def AnalysisData(request):
    assessId=json.loads(request.GET['assess'])
    thisAssess=AssessList.objects.get(AssessId=assessId)
    # 问卷
    if(thisAssess.AssessType==0):
        print("单一问卷")
        myQNaireResults=[]
        myQNaireResults=analysisQNaire(thisAssess)
        return  render(request,"results2.html",{'AnswerList':json.dumps(myQNaireResults)})

    else:
        print("综合评估")
    return render(request, "chooseEva.html")




#def AnalysisData(request):
    #获取问卷id
    #获取问卷所有问题
    #对应问题类型if
    #根据问题id找答卷答案 统计