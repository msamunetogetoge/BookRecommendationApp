from django.shortcuts import render, redirect

from Login.models import M_User

# Create your views here.
def index(request):
    if request.method=="POST":
        id = request.POST["id"]
        password = request.POST["password"]
        if canlogin(id, password):
            return redirect('/book/', permanent=True)
        else:
            return render(request, "index.html", {"msg" :"IDかPASSWORDが間違っています"})
    else:
        return render(request, "index.html")

def signup(request):
    if request.method=="POST":
        id = request.POST["id"]
        password = request.POST["password"]
        name = request.POST["name"]
        email = request.POST["email"]
        user = M_User(id = id, password = password, email = email, name = name)
        if M_User.objects.filter(id=id).exists():
            msg="既に存在しているidです。"
            res ={"msg":msg}
            return render(request, "signup.html", res)
        else:
            user.save()
            return redirect('/book/', permanent=True)
            

    return render(request, "signup.html")

def canlogin(id:str, password:str) -> bool:
        return M_User.objects.filter(id=id, password=password).exists()
