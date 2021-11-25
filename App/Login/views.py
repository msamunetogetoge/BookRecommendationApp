import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseBadRequest
from Books.models import T_Record
from Login.models import M_User, T_Attr
from utils.make_display_data import make_user_config_data

import secrets

# Create your views here.

class SecrectCode:
    def __init__(self):
        self.secret_code=""
secretCode = SecrectCode()

def index(request):
    if request.method=="POST":
        id = request.POST["id"]
        password = request.POST["password"]
        if M_User.objects.filter(username=id, password=password).exists():
            user = M_User.objects.get(username=id, password=password)
            login(request, user)
            return redirect('/book/', permanent=True)
        else:
            return render(request, "index.html", {"msg" :"IDかPASSWORDが間違っています"})
    else:
        return render(request, "index.html")

def logout_user(request):
    """
    ログアウトします
    """
    msg={"msg":""}
    try:
        logout(request)
        return redirect('/book/', permanent=True)
    except:
        msg = {"msg" :"ログアウトに失敗しました"}
        return render(request, "index.html", msg)
        

def change_password(request):
    """
    パスワード変更する
    """
    msg={"msg":""}
    if request.method == "POST":
        print(f"posted = {request.POST['secret_code']}")
        print(f"saved = {secretCode.secret_code }")
        if request.POST["secret_code"] != "" and request.POST["secret_code"] == secretCode.secret_code :
            # password 変更処理
            username = request.POST["username"]
            u = M_User.objects.get(username= username)
            u.password = request.POST["password"]
            u.save()
            msg["msg"] = "パスワードを変更しました。"
            return render(request, "index.html", msg)
        else:
            msg["msg"] ="パスワード変更に失敗しました。"
            return render(request, "change_password.html", msg)
    else:
        return render(request, "change_password.html")

def check_and_publish_code(request):
    """
    Ajax でリクエストが来る想定。
    パスワード変更時、id入力 -> idがあればパスワード入力フォーム表示-> パスワード変更 という流れ。    
    """
    if request.method=="POST":
        id = request.POST["id"]
        if M_User.objects.filter(username=id).exists():
            secretCode.secret_code = secrets.token_hex(16)
            return JsonResponse({"secret":secretCode.secret_code })
        else:
            return HttpResponseBadRequest(request)
    else:
        return redirect('/book/', permanent=True)

def signup(request):
    """
    新規登録画面を返します
    """
    if request.method=="POST":
        id = request.POST["id"]
        password = request.POST["password"]
        name = request.POST["name"]
        email = request.POST["email"]
        user = M_User(username = id, password = password, email = email, name = name)
        if M_User.objects.filter(username=id).exists():
            msg="既に存在しているidです。"
            res ={"msg":msg}
            return render(request, "signup.html", res)
        else:
            user.save()
            login(request, user)
            return redirect('/book/', permanent=True)

    return render(request, "signup.html")

def user_config(request):
    if not request.user.is_authenticated:
        msg ={"msg":"ログインしてください"}
        return render(request, 'index.html', msg)
    else:
        data = make_user_config_data(username=request.user)
        return render(request, "config.html", data)

# この部分はajax にする予定
def register_attr(request):
    """
    ajax 処理で使用する。お気に入りを追加して、画面に表示しなおす為に、データを返す

    Returns:
        [str]: 登録されたお気に入りの名称
    """
    if request.method == "POST":
        code = request.POST.get("code", None)
        if code is None:
            return HttpResponseBadRequest(request)
        else :
            string = request.POST.get("string", "")
            if string != "" and not T_Attr.objects.filter(id=request.user, code=code, string=string).exists():
                attr = T_Attr(id=request.user, code=code, string=string)
                try:
                    attr.save()
                    data = {"string":string}
                    return JsonResponse(data)
                except Exception as e:
                    return HttpResponseBadRequest(request)        
    return HttpResponseBadRequest(request)

def delete_attr(request):
    """
    POSTでリクエストが飛んできた時のみ、T_Attr のデータを削除します
    """
    username = request.user
    if request.method == "POST":
        code  = int(request.POST.get("code",-1))
        string = request.POST.get("string","")
        try:
            attr = T_Attr.objects.get(id=username, code=code, string=string)
            attr.delete()
            data = make_user_config_data(username)
        except Exception as e:
            print(e)
            data = make_user_config_data(username)
            data["msg"] = "削除に失敗"
            return render(request, "config.html", data)
        return render(request, "config.html", data)
    else:
        data = make_user_config_data(username)
        return render(request, "config.html", data)

