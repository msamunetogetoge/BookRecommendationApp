from django.shortcuts import render
from Login.models import M_User
from utils.api_search import search_from_params
from utils.api_search import GoogleBooksStrs

from django.contrib.auth import authenticate, login

# Create your views here.

def book_search(request):
    print(f"user={request.user}")
    if request.method=="POST":
        datas = search_from_params(auth=request.POST["auth"], title=request.POST["title"])
        result ={"datas":datas,"params": GoogleBooksStrs}
        return render(request, "book_search.html", result)

    return render(request, "book_search.html")

def detail(request):
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
        print(result)

        search_result = search_from_params(auth=author)
        data ={"data":result, "search_result": search_result}
        return render(request, "detail.html", data)
    else:
        return render(request, "book_search.html")



       
