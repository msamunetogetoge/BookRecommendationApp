from django.shortcuts import render
from utils.api_search import search_from_params

# Create your views here.
def book_search(request):
    return render(request, "book_search.html")

def search(request):
    if request.method=="POST":
        datas = search_from_params()
        result ={"datas":datas}
        return render(request, "book_search.html", result)
