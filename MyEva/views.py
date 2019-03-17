from django.shortcuts import render
from django.http import HttpResponse
from MyEva.models import UserList
from django.contrib import  messages
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


