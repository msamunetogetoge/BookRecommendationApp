from django.shortcuts import render

from Login.models import M_User

# Create your views here.
def index(request):
    if request.method=="POST":
        id = request.POST["id"]
        password = request.POST["password"]
        if canlogin(id, password):
            return render(request, "index.html", {"msg" :"login許可！"})
        else:
            return render(request, "index.html", {"msg" :"login不可！"})
    else:
        return render(request, "index.html")

def canlogin(id:str, password:str) -> bool:
    try:
        user = M_User.objects.get(id=id, password=password)
        print(f"hello {user.name}")
        return True
    except M_User.DoesNotExist:
        return False
    except Exception:
        return False