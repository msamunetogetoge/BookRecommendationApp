from django.http.response import JsonResponse
from django.shortcuts import render
from Books.models import T_Record
from Login.models import M_User
from utils.api_search import search_from_params, GoogleBooksStrs
from utils.make_display_data import make_user_config_data

from django.contrib.auth import authenticate, login

# Create your views here.

def book_search(request):
    """
    Booksのindex page
    """
    print(f"user={request.user}")
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
                except Exception as e:
                    print(e)
                    author = ""
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
    else:
        return render(request, "book_search.html")

def thoughts(request, title="", authors="", thumbnail=""):
    """[summary]
    感想登録ページ
    """
    if request.method == "POST":
        username = request.user
        title = request.POST.get("title","")
        readdate = request.POST.get("readdate","")
        thoughts = request.POST.get("thoughts","")

        record = T_Record(username=username, title= title, readdate= readdate, thoughts = thoughts)
        try:
            record.save()
            data = make_user_config_data(username)
            return render(request, "config.html",data)
        except Exception as e:
            print(e)
            data = {"title": title, "msg":"保存に失敗しました"}
            return render(request, "thoughts.html", data)
        
    else:
        data = {"title": title, "authors":authors, "thumbnail":thumbnail}
        return render(request, "thoughts.html", data)

       
