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
from MyEva.models import PlanList
from MyEva.models import HeuEvaResult
from MyEva.models import PerformanceRecord
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


def index(request):#测试页面用
      return render(request, "results2.html")

def login(request):#登录
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


def register(request):#注册
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


def indexandmethod(request):#指标与方法库
    HtmlIndexList = []
    HtmlMethodList = []
    MyIndexList = IndexList.objects.values('FatherName', 'Description').distinct()
    MyMethodList = MethodList.objects.values('MethodName','Description').distinct()
    i=0
    for index in MyIndexList:
        tempIndex = {'id':i,'title':'title','content':'content'}
        tempIndex['title']=index['FatherName']
        tempIndex['content']=index['Description'].replace("\n", "<br/>")
        i = i+1
        HtmlIndexList.append(tempIndex)
    j=0
    for method in MyMethodList:
        tempMethod = {'id':j,'title':'title','content':'content'}
        tempMethod['title'] = method['MethodName']
        tempMethod['content'] = method['Description'].replace("\n", "<br/>")
        j = j+1
        HtmlMethodList.append(tempMethod)
    return render(request, "IndexAndMethod.html", {'IndexList': json.dumps(HtmlIndexList),'MethodList':json.dumps(HtmlMethodList)})

def newEva(request):
    return render(request, "newEva.html")

def getIndexInfo():#获取指标信息
    IndexInfo = []
    AllIndexFamilyName = IndexList.objects.all().values('FamilyName').distinct()
    j = 1
    for familyname in AllIndexFamilyName:

        thisFamily = familyname['FamilyName']
        thisFamilyMembers = IndexList.objects.filter(FamilyName=thisFamily)
        tempFamily = {'id': j, 'name': thisFamily, 'FirstList': []}
        Fathers = []
        #统计FatherName
        for member in thisFamilyMembers: #这个家族的成员
            FatherName = member.FatherName
            Fathers.append(FatherName)
        Fathers = set(Fathers)#去重
        k = 1
        for father in Fathers:
            tempFather = {'id': j*10+k, 'listTitle': father, 'selected': [], 'SecondList': []}
            l = 1
            for member in thisFamilyMembers:
                if member.FatherName == father:
                    tempIndex = {'id': j*100+k*10+l, 'listTitle': member.IndexName, 'method': member.thisMethod}
                    tempFather['SecondList'].append(tempIndex)
                    l=l+1
            tempFamily['FirstList'].append(tempFather)
            k=k+1
        IndexInfo.append(tempFamily)
        j=j+1
    return IndexInfo

        


def newBlankEva(request):#新建空白评估
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




def newPlan(Assess,Indexs,Methods):#为评估增加预设方案
    print("新增方案")
    print(Assess)
    thisAssess=AssessList.objects.get(AssessId=Assess['AssessId'])
    indexNum=0
    indexIdList=[]
    temppeople=[]

    for family in Indexs:
        for father in family['FirstList']:
            for selectedIndex in father['selected']:
                indexNum=indexNum+1
                thisMethods=selectedIndex['method'].split(",")
                indexId=IndexList.objects.get(IndexName=selectedIndex['listTitle'])
                indexIdList.append(indexId)
                for thismethod in thisMethods:
                    tempPlanName = "针对" + selectedIndex['listTitle'] + "的"+thismethod
                    PlanList.objects.create(PlanName=tempPlanName,PlanTypeId=thismethod,AssessId=thisAssess)
                    for method in Methods:
                        if(thismethod==method['MethodName']):
                            temppeople.append(method['people'])
    temppeople=list(set(temppeople))
    thisAssess.AssessIndexNum=indexNum
    thisAssess.People=temppeople
    thisAssess.AssessIndexId=indexIdList
    thisAssess.save()
    print("建立方案完毕")
    return True



def getAssessPlan(request):#获取方案用于新建方案的人查看（不包含问卷）
    assessId = json.loads(request.GET['assess'])
    thisAssess=AssessList.objects.get(AssessId=assessId)
    Assess={"AssessId":assessId,"AssessName":thisAssess.AssessName}
    AllPlans=PlanList.objects.filter(AssessId=thisAssess)
    HtmlPlans=[]
    j=1
    for plan in AllPlans:
        temp={"id":j,"PlanId":plan.PlanId,"PlanName":plan.PlanName,"PlanType":plan.PlanTypeId}
        HtmlPlans.append(temp)
        j=j+1
    return  render(request,"editEvaPlan.html",{'Assess':Assess,'plans':HtmlPlans})

def savePlanQNaire(request):#存储新建方案中的新建问卷
    Messages = json.loads(request.body)
    QNaires = Messages['QNaires']
    for QNaire in QNaires:
        PlanId=QNaire['PlanId']
        questions=QNaire['questions']
        thisPlan=PlanList.objects.get(PlanId=PlanId)
        thisAssess=thisPlan.AssessId
        tempSurveyName=str(thisAssess.AssessId)+thisPlan.PlanName
        SurveyList.objects.create(SurveyName=tempSurveyName,SurveyUseNum=thisAssess.AssessUseNum,SurveyQueNum=len(questions),AssessId=thisAssess)
        thisSurvey=SurveyList.objects.get(SurveyName=tempSurveyName,SurveyUseNum=thisAssess.AssessUseNum,SurveyQueNum=len(questions),AssessId=thisAssess)
        thisPlan.PlanTypeId=thisSurvey.SurveyId#将SurveyId对应上Plan
        thisPlan.save()
        for que in questions:
            print(que)
            print(que['type'])
            QueDes = que['title']
            if que['type'] == 'SingleChoose':
                queType = 1
                QuestionList.objects.create(QueDescription=QueDes, QuestionType=queType, isMust=1, SurveyId=thisSurvey)
                thisQuestion = QuestionList.objects.get(QueDescription=QueDes, QuestionType=queType, isMust=1,
                                                        SurveyId=thisSurvey)
                ChoiceList.objects.create(SCQorMCQ=1, ChoiceA=que['ChooseA'], ChoiceB=que['ChooseB'],
                                          ChoiceC=que['ChooseC'], ChoiceD=que['ChooseD'], QuestionId=thisQuestion)
                print("插入成功")
            elif que['type'] == 'MultiChoose':
                queType = 2
                QuestionList.objects.create(QueDescription=QueDes, QuestionType=queType, isMust=1, SurveyId=thisSurvey)
                thisQuestion = QuestionList.objects.get(QueDescription=QueDes, QuestionType=queType, isMust=1,
                                                        SurveyId=thisSurvey)
                ChoiceList.objects.create(SCQorMCQ=2, ChoiceA=que['ChooseA'], ChoiceB=que['ChooseB'],
                                          ChoiceC=que['ChooseC'], ChoiceD=que['ChooseD'], QuestionId=thisQuestion)
            elif que['type'] == 'FillInBlank':
                queType = 3
                QuestionList.objects.create(QueDescription=QueDes, QuestionType=queType, isMust=1, SurveyId=thisSurvey)
            elif que['type'] == 'Scale':
                queType = 4
                QuestionList.objects.create(QueDescription=QueDes, QuestionType=queType, isMust=1, SurveyId=thisSurvey)
                thisQuestion = QuestionList.objects.get(QueDescription=QueDes, QuestionType=queType, isMust=1,
                                                        SurveyId=thisSurvey)
                ScaleList.objects.create(BeginIndex=que['lowest'], EndIndex=que['highest'], DegreeNum=que['ScaleCount'],
                                         QuestionId=thisQuestion)
            elif que['type'] == 'Paragraph':
                queType = 5
                QuestionList.objects.create(QueDescription=QueDes, QuestionType=queType, isMust=1, SurveyId=thisSurvey)
    print("新建方案成功")
    return  render(request,"editEvaPlan.html")

def postAssessInfo(request):#提交方案描述 评估对象等信息
    # description: app.Description,
    # object: app.Object,
    # Assess: app.Assess
    Messages = json.loads(request.body)
    EvaDes=Messages['description']
    EvaObject=Messages['object']
    Assess=Messages['Assess']
    thisAssess=AssessList.objects.get(AssessId=Assess['AssessId'])
    thisAssess.AssessDes=EvaDes
    thisAssess.AssessObject=EvaObject
    thisAssess.save()
    return render(request,"editEva2.html")



def getEvaInfo(request):#新建评估中 获取选择的指标
    global ASSESS
    global INDEXS
    INDEXS=[]
    print(request.body)
    Messages = json.loads(request.body)
    ASSESS = Messages['Assess']
    INDEXS = Messages['Indexs']#复杂嵌套数据用request.body
    methods = MethodList.objects.all()
    htmlMethods = []
    for method in methods:
        temp = {'MethodId': method.MethodId, 'MethodName': method.MethodName, 'dataSource': method.dataSource,
                'dealData': method.dealData, 'people': method.people}
        htmlMethods.append(temp)
    print(ASSESS)
    newPlan(ASSESS,INDEXS,htmlMethods)
    methods = MethodList.objects.all()
    print(INDEXS)
    return  render(request,"editEva2.html",{'Assess':ASSESS,'Index':INDEXS,'Method':htmlMethods})


def showEvaInfo(request):#新建评估中将指标和方法等信息展示
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



def addQNaire(request):#新建问卷的问题
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
        ThisQNaire.SurveyQueNum=len(Questions)
        ThisQNaire.save()
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



def chooseEva(request):#展示评估方案列表
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




def getFillAssess(request):#录入评估数据
    #assessId = json.loads(request.body)
    assessId=json.loads(request.GET['assess'])
    #先get到assess的id
    Assess=AssessList.objects.get(AssessId=assessId)
    if Assess.AssessType == 0:#录入问卷
        HtmlQuestionsList=[]
        Survey=SurveyList.objects.get(AssessId=Assess.AssessId)
        Questions=QuestionList.objects.filter(SurveyId=Survey)
        print(type(Questions))
        j=1
        for que in Questions:

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
    else:#是综合评估
        HtmlAssess = {"AssessId": assessId, "AssessName": Assess.AssessName}
        AllPlans = PlanList.objects.filter(AssessId=Assess)
        HtmlPlans = []
        j = 1
        HtmlQNaires = []
        for plan in AllPlans:
            temp = {"id": j, "PlanId": plan.PlanId, "PlanName": plan.PlanName, "PlanType": plan.PlanTypeId}
            if (str(plan.PlanTypeId).isdigit()):  # 判断里面是不是数字，是的话则为survey
                temp['PlanType']="可用性测试"
                HtmlQuestionsList = []
                surveyId = plan.PlanTypeId
                thisSurvey = SurveyList.objects.get(SurveyId=surveyId)
                Questions = QuestionList.objects.filter(SurveyId=thisSurvey)
                print(type(Questions))
                q = 1
                for que in Questions:

                    if que.QuestionType == 1:
                        tempQue = {'id': q, 'queId': '', 'title': 'title', 'type': 'SingleChoose', 'ChooseA': '',
                                   'ChooseB': '', 'ChooseC': '', 'ChooseD': '', "answer": ''}
                        tempQue['queId'] = que.QuestionId
                        tempQue['title'] = que.QueDescription
                        choices = ChoiceList.objects.get(QuestionId=que)
                        tempQue['ChooseA'] = choices.ChoiceA
                        tempQue['ChooseB'] = choices.ChoiceB
                        tempQue['ChooseC'] = choices.ChoiceC
                        tempQue['ChooseD'] = choices.ChoiceD
                        HtmlQuestionsList.append(tempQue)
                        q = q + 1
                    elif que.QuestionType == 2:
                        tempQue = {'id': q, 'queId': '', 'title': 'title', 'type': 'MultiChoose', 'ChooseA': '',
                                   'ChooseB': '', 'ChooseC': '', 'ChooseD': '', 'answer': []}
                        tempQue['queId'] = que.QuestionId
                        tempQue['title'] = que.QueDescription
                        choices = ChoiceList.objects.get(QuestionId=que)
                        tempQue['ChooseA'] = choices.ChoiceA
                        tempQue['ChooseB'] = choices.ChoiceB
                        tempQue['ChooseC'] = choices.ChoiceC
                        tempQue['ChooseD'] = choices.ChoiceD
                        HtmlQuestionsList.append(tempQue)
                        q = q + 1
                    elif que.QuestionType == 3:
                        tempQue = {'id': q, 'queId': '', 'title': 'title', 'type': 'FillInBlank', 'answer': ''}
                        tempQue['queId'] = que.QuestionId
                        tempQue['title'] = que.QueDescription
                        HtmlQuestionsList.append(tempQue)
                        q = q + 1
                    elif que.QuestionType == 4:
                        tempQue = {'id': q, 'queId': '', 'title': 'title', 'type': 'Scale', 'lowest': 'lowest',
                                   'highest': 'highest', 'ScaleCount': 0, 'answer': ''}
                        tempQue['queId'] = que.QuestionId
                        tempQue['title'] = que.QueDescription
                        scale = ScaleList.objects.get(QuestionId=que)
                        tempQue['lowest'] = scale.BeginIndex
                        tempQue['highest'] = scale.EndIndex
                        tempQue['ScaleCount'] = scale.DegreeNum
                        HtmlQuestionsList.append(tempQue)
                        q = q + 1
                    elif que.QuestionType == 5:
                        # "id": 3, "title": "嘻嘻嘻嘻", "type": "Paragraph"
                        tempQue = {'id': q, 'queId': '', 'title': 'title', 'type': 'Paragraph'}
                        tempQue['queId'] = que.QuestionId
                        tempQue['title'] = que.QueDescription
                        HtmlQuestionsList.append(tempQue)
                        q = q + 1
                print(HtmlQuestionsList)
                tempQNaire = {"PlanId": plan.PlanId, "Question": HtmlQuestionsList}
                HtmlQNaires.append(tempQNaire)
            HtmlPlans.append(temp)
            j = j + 1
        return render(request, "evaPlan.html", {'Assess': HtmlAssess, 'plans': HtmlPlans, 'QNaires': HtmlQNaires})



def FillQNaire(request):#填写问卷
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



def deleteAssess(request):#删除评估方案
    Messages = json.loads(request.body)
    assessId = Messages['assess']
    AssessList.objects.filter(AssessId=assessId).delete()
    print("删除成功")
    return  render(request,"chooseEva.html")

def countFrequency(answers):#计算词频
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

def analysisQNaire(thisSurvey):#分析问卷结果
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
            for i in range(0,thisScale.DegreeNum):
                chooseNum.append(0)
            print("长度")
            print(len(chooseNum))
            completePeople=0
            for thisAns in thisAnswers:
                if thisAns.QuestionId==que:
                    completePeople=completePeople+1
                    choosed=ScaleAnswerList.objects.get(AnswerId=thisAns)
                    print("下标")
                    print(choosed.DegreeAnswer-1)
                    chooseNum[choosed.DegreeAnswer-1]=chooseNum[choosed.DegreeAnswer-1]+1
            chooseRatio=[]
            for i in range(0,thisScale.DegreeNum):
                chooseRatio.append(chooseNum[i]/completePeople)
            degree=[]
            degree=(numpy.arange(1, thisScale.DegreeNum+1, 1)).tolist()
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

def getEvaAnswer(request):#获取用户填的评估数据
    message = json.loads(request.body)
    print(message)
    Assess=message['Assess']
    AllInfo=message['AllInfo']
    AssessId=Assess['AssessId']
    global USER

    thisAssess=AssessList.objects.get(AssessId=AssessId)
    assessedNum = math.ceil((thisAssess.AssessUseNum * thisAssess.AssessPro) / 100)  # 向上取整
    assessedNum = assessedNum + 1
    assessPro = assessedNum * 100 / thisAssess.AssessUseNum
    if (assessPro > 100):
        assessPro = 100
    thisAssess.AssessPro = assessPro
    thisAssess.save()

    for info in AllInfo:
        PlanId=info['Planid']
        PlanType=info['PlanType']
        thisPlan=PlanList.objects.get(PlanId=PlanId)
        IndexName=thisPlan.PlanName[2:].split('的')[0]#截取“针对”之后，“的”之前
        thisIndex=IndexList.objects.get(IndexName=IndexName)
        if(PlanType=="启发式评估"):
                UseTables=[]
                UseTables=info['UseTables']
                for usetable in UseTables:
                    HeuEvaResult.objects.create(Interface=usetable['local'],HeuProblem=usetable['problem'],SeriousDegree=usetable['serious'],Advice=usetable['advice'],IndexId=thisIndex,PlanId=thisPlan,UserId=USER)
        elif(PlanType=="数据记录"):
                print("录入数据记录！")
                dataInfo=[]
                dataInfo=info['myInfo'].split(',')
                PerformanceRecord.objects.create(ErrorRate=float(dataInfo[0]),FinishTime=float(dataInfo[1]),SuccessRate=float(dataInfo[2]),LookingTime=float(dataInfo[3]),PlanId=thisPlan,UserId=USER)
        elif(PlanType=="可用性测试"):
                Answers=info['QNaireInfo']
                surveyId=thisPlan.PlanTypeId
                thisSurvey=SurveyList.objects.get(SurveyId=surveyId)
                thisPaper = PaperList.objects.filter(UserId=USER, SurveyId=thisSurvey)
                if thisPaper.exists():
                    print("您已填过该评估方案！不可重复填写！")
                    messages.error(request, "您已填过该评估方案！不可重复填写！")
                    return render(request, "chooseEva.html")
                else:
                    # 增加一个填问卷的人
                    surveyedNum = math.ceil((thisSurvey.SurveyUseNum * thisSurvey.SurveyPro) / 100)
                    print(surveyedNum)
                    surveyedNum = surveyedNum + 1
                    print(surveyedNum)
                    pro = surveyedNum * 100 / thisSurvey.SurveyUseNum
                    print(pro)
                    if (pro > 100):
                        pro = 100
                    thisSurvey.SurveyPro = pro
                    thisSurvey.save()


                    PaperList.objects.create(UserId=USER, SurveyId=thisSurvey)
                    thisPaper = PaperList.objects.get(UserId=USER, SurveyId=thisSurvey)
                    for ans in Answers:
                        print(type(ans))
                        print(ans['queId'])
                        thisQuestion = QuestionList.objects.get(QuestionId=ans['queId'])
                        if ans['type'] == 'SingleChoose':  # 单选题
                            AnswerList.objects.create(QuestionType=1, isMust=1, PaperId=thisPaper,
                                                      QuestionId=thisQuestion)
                            thisAnswer = AnswerList.objects.get(QuestionType=1, isMust=1, PaperId=thisPaper,
                                                                QuestionId=thisQuestion)
                            SCAList.objects.create(ChoiceAnswer=ans['answer'], AnswerId=thisAnswer)
                        elif ans['type'] == 'MultiChoose':  # 多选题
                            AnswerList.objects.create(QuestionType=2, isMust=1, PaperId=thisPaper,
                                                      QuestionId=thisQuestion)
                            thisAnswer = AnswerList.objects.get(QuestionType=2, isMust=1, PaperId=thisPaper,
                                                                QuestionId=thisQuestion)
                            MCAanswers = ','.join(ans['answer'])
                            MCAList.objects.create(ChoiceAnswer=MCAanswers, ChoiceNum=len(ans['answer']),
                                                   AnswerId=thisAnswer)
                        elif ans['type'] == 'FillInBlank':  # 填空题
                            AnswerList.objects.create(QuestionType=3, isMust=1, PaperId=thisPaper,
                                                      QuestionId=thisQuestion)
                            thisAnswer = AnswerList.objects.get(QuestionType=3, isMust=1, PaperId=thisPaper,
                                                                QuestionId=thisQuestion)
                            print(ans['answer'])
                            FIBAnswerList.objects.create(FIBAnswer=ans['answer'], AnswerId=thisAnswer)
                        elif ans['type'] == 'Scale':  # 量表题
                            AnswerList.objects.create(QuestionType=4, isMust=1, PaperId=thisPaper,
                                                      QuestionId=thisQuestion)
                            thisAnswer = AnswerList.objects.get(QuestionType=4, isMust=1, PaperId=thisPaper,
                                                                QuestionId=thisQuestion)
                            ScaleAnswerList.objects.create(DegreeAnswer=ans['answer'], AnswerId=thisAnswer)
                        elif ans['type'] == 'Paragraph':
                            print("段落")
        else:
            print("暂未开发")


    return render(request,"evaPlan.html")

# id:1,
# 		serious:3,
# 		problem:"31xxx",
# 		local:"31xxxx",
# 		advice:"31xxxxx"









def AnalysisData(request):#分析评估数据
    assessId=json.loads(request.GET['assess'])
    thisAssess=AssessList.objects.get(AssessId=assessId)
    # 问卷
    if(thisAssess.AssessType==0):
        print("单一问卷")
        myQNaireResults=[]
        thisSurvey = SurveyList.objects.get(AssessId=assessId)
        myQNaireResults=analysisQNaire(thisSurvey)
        return  render(request,"results2.html",{'AnswerList':json.dumps(myQNaireResults)})

    else:#综合评估
        thisPlans = PlanList.objects.filter(AssessId=thisAssess)
        HtmlPlanList = []
        allUseProblems = []
        QNaireResults = []
        ErrorRate = 0
        FinishTime = 0
        SuccessRate = 0
        LookingTime = 0
        usernum = 0

        j=1
        for plan in thisPlans:


            if plan.PlanTypeId == '启发式评估':
                temp = {"id": j, "PlanId": plan.PlanId, "PlanName": plan.PlanName, "PlanType": plan.PlanTypeId}
                HtmlPlanList.append(temp)
                j = j + 1
                # 列出可用性问题清单
                thisHeus = HeuEvaResult.objects.filter(PlanId=plan).order_by('SeriousDegree')
                heucount = 1
                useProblems = []
                for heu in thisHeus:
                    tempHeu = {'id': heucount, 'serious': heu.SerioueDegree, 'problem': heu.HeuProblem,
                               'local': heu.Interface, 'advice': heu.Advice}
                    useProblems.append(tempHeu)
                    heucount = heucount + 1
                tempPlanHeu = {'PlanId': plan.PlanId, 'useProblems': useProblems}
                allUseProblems.append(tempPlanHeu)
            elif plan.PlanTypeId == '数据记录':
                temp = {"id": j, "PlanId": plan.PlanId, "PlanName": plan.PlanName, "PlanType": plan.PlanTypeId}
                HtmlPlanList.append(temp)
                j = j + 1
                # 算出平均值
                thisPerformance = PerformanceRecord.objects.filter(PlanId=plan)
                usernum = len(thisPerformance)
                for performance in thisPerformance:
                    ErrorRate = ErrorRate + performance.ErrorRate
                    FinishTime = FinishTime + performance.FinishTime
                    SuccessRate = SuccessRate + performance.SuccessRate
                    LookingTime = LookingTime + performance.LookingTime
            elif (str(plan.PlanTypeId).isdigit()):  # 可用性测试
                temp = {"id": j, "PlanId": plan.PlanId, "PlanName": plan.PlanName, "PlanType": "可用性测试"}
                HtmlPlanList.append(temp)
                j = j + 1
                thisSurveyId = plan.PlanTypeId
                thisSurvey = SurveyList.objects.get(SurveyId=thisSurveyId)
                ResultsData = analysisQNaire(thisSurvey)
                tempQNairePlan = {'PlanId': plan.PlanId, 'ResultsData': ResultsData}
                QNaireResults.append(tempQNairePlan)
            else:
                print("主观量表，暂未开发")
        HtmlInfoList = [{'name': '出错频率', 'unit': '次/小时', 'data': ErrorRate / usernum},
                        {'name': '完成时间', 'unit': '分钟', 'data': FinishTime / usernum},
                        {'name': '成功率', 'unit': '%', 'data': SuccessRate / usernum},
                        {'name': '平均注视时间 ', 'unit': '秒', 'data': LookingTime / usernum}]
        return  render(request,"EvaResult.html",{'PlanList':HtmlPlanList,'infoList':HtmlInfoList,'QNaireResults':QNaireResults,'allUseProblems':allUseProblems})
    return render(request, "chooseEva.html")





