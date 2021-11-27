from django import utils
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from Books.models import T_Record
from Login.models import M_User
from utils.api_search import search_from_params, GoogleBooksStrs
from utils.make_display_data import make_user_config_data
from utils.need_login import need_login

from django.contrib.auth import authenticate, login

import datetime

# Create your views here.

def book_search(request):
    """
    Booksのindex page
    """
    if request.method=="POST":
        datas = search_from_params(auth=request.POST["auth"], title=request.POST["title"])
        result ={"datas":datas,"params": GoogleBooksStrs}
        return render(request, "book_search.html", result)

    return render(request, "book_search.html")


def detail(request):
    """
    本の詳細ページ
    """
    if request.method =="POST":
        result = {}
        for k in GoogleBooksStrs.result_keys:
            if k == GoogleBooksStrs.authors:
                try:
                    author = eval(request.POST[k])[0]
                    if(author == ""):
                        author = "noinfo"
                except Exception as e:
                    print(e)
                    author = "noinfo"
                result[k] = author
            elif k == GoogleBooksStrs.imageLinks:
                try:
                    thumbnail = eval(request.POST[k])
                except Exception as e:
                    print(e)
                    thumbnail = {'thumbnail':"/static/noimage.png"}
                result[k] = thumbnail
            elif k in request.POST.keys():
                result[k]=request.POST[k]

        search_result = search_from_params(auth=author)
        data ={"data":result, "search_result": search_result}
        return render(request, "detail.html", data)
    
    return render(request, "book_search.html")


@need_login(redirect_field_name="index.html", err_msg="登録にはログインが必要です。")
def thoughts(request, title="", authors="", thumbnail=""):
    """[summary]
    感想登録
    """
    if request.method == "POST":
        username = str(request.user)
        title = request.POST.get("title","")
        readdate = request.POST.get("readdate", utils.timezone.now())
        thoughts = request.POST.get("thoughts","")
        readflag = eval(request.POST.get("readflag","True"))
        try:
            record, is_created = T_Record.objects.get_or_create(username=username, title= title)
            record.readdate = readdate
            record.thoughts = thoughts
            record.readflag = readflag
            record.save()
            data = make_user_config_data(username)
            return render(request, "config.html",data)
        except Exception as e:
            print(e)
            data = {"title": title, "msg":"保存に失敗しました"}
            return render(request, "config.html",data)
        
    data = {"title":title, "authors":authors, "thumbnail":thumbnail}
    return render(request, "detail.html", data)

def readend(request):
    """
    読みたい本を既読本にする。
    """
    username = request.user
    if request.method == "POST":
        title = request.POST.get("title","")
        print(f"title={title}, uer={username}")
        try:
            record = T_Record.objects.get(username=username, title=title)
            record.readflag = True
            record.readdate = utils.timezone.now()
            record.save()
            data = make_user_config_data(username)
            
        except Exception as e:
            print(e)
            data = make_user_config_data(username)
            data["msg"] = "更新に失敗しました"
            
        return render(request, "config.html",data)
    else:
        data = make_user_config_data(username)
        return render(request, "config.html",data)

def delete_not_read(request):
    """
    読みたい本を削除する
    """
    username = request.user
    if request.method == "POST":
        title = request.POST.get("title","")
        print(f"title={title}, uer={username}")
        try:
            record = T_Record.objects.get(username=username, title=title)
            record.delete()
            data = make_user_config_data(username)
            
        except Exception as e:
            print(e)
            data = make_user_config_data(username)
            data["msg"] = "削除に失敗しました"
            
        return render(request, "config.html",data)
    else:
        data = make_user_config_data(username)
        return render(request, "config.html",data)
