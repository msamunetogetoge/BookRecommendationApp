import requests, json


class GoogleBooksStrs:
    """
    google book apiからデータを取り出すときに使う文字列を定義するクラス
    """
    totalitems = "totalitems"
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
    result_keys = [title, authors, publisheddate, pagecount, industryIdentifiers, imageLinks, description]
    #imagelink, thumbnail も追加する
    

def search_from_params(auth:str="", title:str="")->list[dict]:
    """[summary]
    作者、題名をクエリパラメータとして、googlebooks api でデータを検索する。
    Args:
        auth (str, optional): 題名. Defaults to "".
        title (str, optional): 作者. Defaults to "".

    Returns:
        [list[dict]]: dict のkey はGoogleBooksStrs.result_keys
        auth, titleが空の時は空のリストを返す
    """
    url = create_query_string(auth=auth, title=title)
    if url == "":
        return list({})
    res = requests.get(url).json()
    result_list = get_result_list(res)
    return result_list
    


def create_query_string(title="", auth="")->str:
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
    print(url)
    return url
def get_result_list(response:dict)-> list[dict]:
    if response['totalItems'] == 0:
        return list({})
    result_dict =[]
    items = response["items"]
    for item in items:
        item_volume = item[GoogleBooksStrs.volumeinfo]
        print(item_volume)
        dic = {}
        for k in GoogleBooksStrs.result_keys:
            if k in item_volume.keys():
                dic[k]=item_volume[k]
            elif k not in item_volume.keys() and  k == GoogleBooksStrs.industryIdentifiers :
                dic[k] = []
            elif k not in item_volume.keys() and  k == GoogleBooksStrs.imageLinks:
                dic[k] = {'thumbnail':"/static/noimage.png"}
            else:
                dic[k] = ""
        result_dict.append(dic)
    return result_dict


