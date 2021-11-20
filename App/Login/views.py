import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseBadRequest

from Login.models import M_User, T_Attr

# Create your views here.
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
    msg={"msg":""}
    try:
        logout(request)
    except:
        msg = {"msg" :"ログアウトに失敗しました"}
        # msg = {"msg" :e}
    finally:
        return render(request, "index.html", msg)

def signup(request):
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

def make_user_config_data(username:str) -> dict:
    """
    username からT_Attrを検索する

    Args:
        username (str): M_User.username

    Returns:
        dict: {"name": name, "auth": auth:list, "genre": genre:list} の形の辞書
    """
    user = M_User.objects.get(username = username)
    name = user.name
    auth = list(T_Attr.objects.filter(id=user.username, code=0).order_by("string").values_list('string', flat=True))
    genre = list(T_Attr.objects.filter(id=user.username, code=1).order_by("string").values_list('string', flat=True))
    data ={"name": name, "auth": auth, "genre": genre}
    return data