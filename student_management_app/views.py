from django.shortcuts import render
#from channels.auth import login
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from student_management_app.EmailBackEnd import EmailBackEnd
from django.contrib import messages
# Create your views here.
def showDemoPage(request):
    return render(request,"demo.html")

# login page
def ShowLoginPage(request):
    return render(request, "login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    else:
        user=authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect('/staff_home')
            else:
                return HttpResponseRedirect('/student_home')
        else:
            messages.error(request,"Invalid login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : " +request.user.email+"usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")




def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")