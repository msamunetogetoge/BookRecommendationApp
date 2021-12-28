import inspect
import requests, json


class GoogleBooksStrs:
    """
    google book apiからデータを取り出すときに使う文字列を定義するクラス
    """
    totalitems = "totalItems"
    volumeinfo = "volumeInfo"
    title = "title"
    authors = "authors"
    publisheddate = "publishedDate"
    pagecount = "pageCount"
    industryIdentifiers = 'industryIdentifiers'
    type = 'type'
    identifier = "identifier"
    imageLinks = "imageLinks"
    description = 'description'
    thumbnail = "thumbnail"
    result_keys = [title,totalitems, authors, publisheddate, pagecount, industryIdentifiers, imageLinks, description]
    

def search_from_params(auth:str="", title:str="", startindex:int=0)->list[dict]:
    """[summary]
    作者、題名をクエリパラメータとして、googlebooks api でデータを検索する。
    Args:
        auth (str, optional): 題名. Defaults to "".
        title (str, optional): 作者. Defaults to "".

    Returns:
        [list[dict]]: dict のkey はGoogleBooksStrs.result_keys
        auth, titleが空の時は空のリストを返す
    """
    url = create_query_string(auth=auth, title=title, startindex=startindex)
    if url == "":
        return list({})
    res = requests.get(url).json()
    result_list = get_result_list(res, auth)
    return result_list
    


def create_query_string(title:str="", auth:str="", startindex:int=0)->str:
    """
    googlebooksapiでデータを取得する為のurlを作成する

    Args:
        auth (str, optional): 作者. Defaults to "".
        title (str, optional): 本の題名. Defaults to "".

    Returns:
        [str]: url
    """
    url = 'https://www.googleapis.com/books/v1/volumes?q='
    if auth =="" and title == "":
        return ""
    elif auth != "" and title =="":
        q1 = "inauthor:" + auth
        url += q1
    elif auth == "" and title != "":
        q2 = "intitle:" + title
        url += q2
    else:
        q1 = "inauthor:" + auth
        q2 = "intitle:" + title
        url+= q1 + "+" + q2
    url +=  "&maxResults=40"
    url += f"&startIndex={startindex}"
    return url

def get_result_list(response:dict, author:str="", startIndex:int=0)-> list[dict]:
    """[summary]GoogleBooksApiで取ってきたjsonデータを使いやすい形にまとめる関数

    Args:
        response (dict): GoogleBooksApi で取ってきたデータ
        author (str, optional): 著者を指定したい時の変数 Defaults to "".
        startIndex (int, optional): startIndexに指定する値. Defaults to 0.

    Returns:
        list[dict]: GoogleBooksStrs.result_keys に指定されている値をkeyにした辞書をlistにする
    """
    totalitems = GoogleBooksStrs.totalitems
    result_dict =[]
    items = response.get("items", None)

    # データが無い時は空データを返す
    if items == None:
        return list({})

    for item in items:
        item_volume = item[GoogleBooksStrs.volumeinfo]
        dic = {}
        dic[totalitems] = response[totalitems]
        for k in GoogleBooksStrs.result_keys:
            if k in item_volume.keys():
                dic[k]=item_volume[k]
            elif k not in item_volume.keys() and  k == GoogleBooksStrs.industryIdentifiers :
                dic[k] = []
            elif k not in item_volume.keys() and  k == GoogleBooksStrs.imageLinks:
                dic[k] = {'thumbnail':"/static/noimage.png"}
            elif k == GoogleBooksStrs.totalitems :
                pass
            else:
                dic[k] = ""
        # authors はリストからstr(カンマ区切り)にする
        if len(dic[GoogleBooksStrs.authors]) > 1:
            dic[GoogleBooksStrs.authors] =",".join(dic[GoogleBooksStrs.authors])
        elif len(dic[GoogleBooksStrs.authors]) == 1:
            dic[GoogleBooksStrs.authors] =dic[GoogleBooksStrs.authors][0]

        # author 指定がある時は、authorが空の場所にauthorを挿入する
        if author != "" and ( dic[GoogleBooksStrs.authors] in [[], None, ""]):
            dic[GoogleBooksStrs.authors] = author

        result_dict.append(dic)
    return result_dict


