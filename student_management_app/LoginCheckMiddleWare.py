from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse 



class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "student_management_app.hod_views":
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))

            elif user.user_type == "2":
                if modulename == "student_management_app.staff_views" :
                    pass
                elif modulename == "student_management_app.views" or modulename == "django.views.static":
                    pass
                else:
                   return HttpResponseRedirect(reverse("staff_home"))

            elif user.user_type == "3":
                if modulename == "student_management_app.student_views" or modulename == "django.views.static":
                    pass
                elif modulename == "student_management_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))

            else:
                return HttpResponseRedirect(reverse("show_login"))  
                
                          
        else:
            if request.path == reverse("show_login") or request.path == reverse("doLogin") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))