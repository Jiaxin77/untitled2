from django.shortcuts import render
from django.http import HttpResponse
from MyEva.models import UserList
from MyEva.models import MethodList
from MyEva.models import IndexList
from django.contrib import  messages
import json
# Create your views here.



def index(request):
      return render(request, "login.html", {"message": ""})

def login(request):
    result = ""
    if request.method == "POST":
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        if UserList.objects.filter(UserName=username):
            if UserList.objects.filter(Password=password):
                result = "登录成功"
                #messages.success(request,"登录成功")
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
    print("laile!!")
    HtmlIndexList=[]
    HtmlMethodList=[]
    MyIndexList = IndexList.objects.values('FatherName', 'Description').distinct()
    MyMethodList = MethodList.objects.values('MethodName','Description').distinct()
   # print(type(MyIndexList))
   # print(MyIndexList)
    i=0
    for index in MyIndexList:
       # print(index)
        tempIndex={'id':i,'title':'title','content':'content'}
        tempIndex['title']=index['FatherName']
        tempIndex['content']=index['Description'].replace("\n","<br/>")
      #  print(tempIndex)
        i=i+1
        HtmlIndexList.append(tempIndex)
    j=0
    for method in MyMethodList:
        tempMethod={'id':j,'title':'title','content':'content'}
        tempMethod['title']=method['MethodName']
        tempMethod['content']=method['Description'].replace("\n","<br/>")
        j=j+1
        HtmlMethodList.append(tempMethod)
    print(HtmlIndexList)
    print(HtmlMethodList)
    return render(request, "IndexAndMethod.html",{'IndexList':json.dumps(HtmlIndexList),'MethodList':json.dumps(HtmlMethodList)})


