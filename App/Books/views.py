from django.shortcuts import render
from utils.api_search import search_from_params
from utils.api_search import GoogleBooksStrs

# Create your views here.
def book_search(request):
    if request.method=="POST":
        datas = search_from_params(auth=request.POST["auth"], title=request.POST["title"])
        result ={"datas":datas,"params": GoogleBooksStrs}
        return render(request, "book_search.html", result)

    return render(request, "book_search.html")

