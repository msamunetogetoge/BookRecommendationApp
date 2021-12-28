import inspect
from typing import Counter
from django import utils
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from Books.models import T_Record
from Login.models import M_User
from utils.api_search import search_from_params, GoogleBooksStrs
from utils.make_display_data import make_user_config_data
from utils.need_login import need_login

# Create your views here.
class SearchCounter:
    """[summary]
    本を検索した時に、startIndex > allItems になってエラーを出さないようにするためのクラス
    """
    allitems:int
    def __init__(self):
        self.allitems = 200

    def change_counter(self, allitem:int):
        """[summary]
            allItemsの値を更新する(小さい時だけ更新)
        Args:
            allitem (int): GoogleBooksApiの検索結果の数
        """
        if self.allitems < allitem:
            self.allitems = allitem
        return
    
    def canSearch(self, startIndex:int)->bool:
        """[summary]

        Args:
            startIndex (int): クエリに含めるstartIndexの値

        Returns:
            bool: startIndex < totalItems ならTrue
        """
        return startIndex < self.allitems
    
counter = SearchCounter()

def book_search(request):
    """
    Booksのindex page 
    Post なら検索結果をJspnで返す
    Getなら検索ページを表示する
    """
    if request.method=="POST":
        try:
            author = request.POST.get("author","")
            title = request.POST.get("title","")
            startindex = 40 * int(request.POST.get("next_int","0"))

            # 検索を続けた時に、 startIndex > totalItems となるとエラーになるので回避する処理    
            if startindex == 0:
                datas = search_from_params(auth=author, title=title, startindex=startindex)
            elif counter.canSearch(startindex):
                datas = search_from_params(auth=author, title=title, startindex=startindex)
            else:
                datas = list({})
            
            result = {"datas":datas}
            if len(datas) == 0:
                response = JsonResponse({"error": "検索結果が0件です"})
                response.status_code = 500
                return response
            
            # totalItems の数を更新する
            counter.change_counter(int(datas[0][GoogleBooksStrs.totalitems]))
            return JsonResponse(result)
        except Exception as e:
            print(f"{inspect.currentframe().f_back.f_code.co_filename},{inspect.currentframe().f_back.f_lineno},{e}")
            response = JsonResponse({"error": "検索時エラーが起きました。再度検索してみてください。"})
            response.status_code = 500
            return response
        
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
                    author = request.POST[k]
                except Exception as e:
                    print(f"{inspect.currentframe().f_back.f_lineno},{e}")
                    author = "noinfo"
                result[k] = author
            elif k == GoogleBooksStrs.imageLinks:
                try:
                    thumbnail = eval(request.POST[k])
                except Exception as e:
                    print(f"{inspect.__name__},{inspect.currentframe().f_back.f_lineno},{e}")
                    thumbnail = {'thumbnail':"/static/noimage.png"}
                result[k] = thumbnail
            elif k in request.POST.keys():
                result[k]=request.POST[k]
        search_result = search_from_params(auth=author)
        data ={"data":result, "search_result": search_result}
        return render(request, "detail.html", data)
    
    return render(request, "book_search.html")


@need_login(redirect_field_name="index.html", err_msg="登録にはサインアップ、ログインが必要です。")
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
            print(f"{inspect.currentframe().f_back.f_code.co_filename},{inspect.currentframe().f_back.f_lineno},{e}")
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
            print(f"{inspect.currentframe().f_back.f_code.co_filename},{inspect.currentframe().f_back.f_lineno},{e}")
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
            print(f"{inspect.currentframe().f_back.f_code.co_filename},{inspect.currentframe().f_back.f_lineno},{e}")
            data = make_user_config_data(username)
            data["msg"] = "削除に失敗しました"
            
        return render(request, "config.html",data)
    else:
        data = make_user_config_data(username)
        return render(request, "config.html",data)
