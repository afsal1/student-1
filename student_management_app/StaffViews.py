from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import Subjects, SessionYearModel, Students, FeedbackStudent,Staffs, LeaveReportStaff, FeedbackStaffs, Attendance, AttendanceReport, CustomUser,Courses, Attendance, StudentResult
from django.core import serializers
import json
from django.urls import reverse
from django.contrib import messages
from datetime import date





def staff_home(request):
    #fetch all students under staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_list_id=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_list_id.append(course.id)

    final_course=[]
    #remove duplicate course course id 
    for course_id in course_list_id:
        if course_id not in final_course:
            final_course.append(course_id)
    students_count=Students.objects.filter(course_id__in=final_course).count()

    #fetch the attendance count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #fetch the approve leave count
    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()

    subject_count=subjects.count()

    #fetch attendance data by subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name) 
        attendance_list.append(attendance_count1) 

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)
    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subject_count":subject_count,"attendance_list":attendance_list,"subject_list":subject_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})

def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years = SessionYearModel.objects.all()
    today=date.today()
    date1= today.strftime("%d-%m-%Y")
    print(date1)
    return render(request,"staff_template/staff_take_attendance copy.html",{"subjects":subjects,"session_years":session_years,"date1":date1}) 


# def staff_view_attendance(request):
#     subjects=Subjects.objects.all()
#     session_year_id = SessionYearModel.objects.all()
#     return render(request,"staff_template/staff_take123_attendance copy.html",{"subjects":subjects,"session_year_id":session_year_id})




@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject") 
    session_year = request.POST.get("session_year")

    
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year)
    students=Students.objects.filter(course_id=subject_model.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json",safe=False)


#return HttpResponse(students)
#student_data=serializers.serialize("python",students)
    


@csrf_exempt
def put_students(request):
    subject_id = request.POST.get("subject") 
    session_year = request.POST.get("session_year")

    
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year)
    students=Students.objects.filter(course_id=subject_model.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json",safe=False)



@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")


    subject_model=Subjects.objects.get(id=subject_id)
    session_year_model=SessionYearModel.objects.get(id=session_year_id)
    json_student=json.loads(student_ids)
    #print(data[0]['id'])


    try:
    

        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_year_model)
        attendance.save()

        for stud in json_student:
            student=Students.objects.get(admin=stud['id'])
            attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
            attendance_report.save()        
        return HttpResponse("OK")
    except:
        return HttpResponse("ERROR")




def staff_update1_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_update_attendance copy.html",{"subjects":subjects,"session_year_id":session_year_id})


@csrf_exempt
def put_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data) 


    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def put_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")

    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)






def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id = SessionYearModel.objects.all()
    return render(request, "staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})


@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data) 


    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")

    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)





@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    json_student=json.loads(student_ids)



    try:
        for stud in json_student:
            student=Students.objects.get(admin=stud['id'])
            attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
            attendance_report.status=stud['status']
            attendance_report.save()
        return HttpResponse("OK")

    except:
        return HttpResponse("ERROR")


def staff_apply_leave(request):
    staff_obj=Staffs.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})



def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_meassage=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request,"Failed to Apply Leave")
            return HttpResponseRedirect(reverse("staff_apply_leave"))




def staff_feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedbackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})



def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            feedback=FeedbackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request,"Successfully Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request,"Failed to Send Feedback")
            return HttpResponseRedirect(reverse("staff_feedback"))




def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})



def staff_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_profile"))

    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request,"Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request,"Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))



def staff_add_result(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.objects.all()
    return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})


def save_student_result(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_add_result"))
    student_admin_id=request.POST.get('student_list')
    assignment_marks=request.POST.get('assignment_marks')
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')


    student_obj=Students.objects.get(admin=student_admin_id)
    subject_obj=Subjects.objects.get(id=subject_id)
    try:
        check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_assignment_marks=assignment_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request,"Successfully Updated Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
        else:
            result=StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
            result.save()
            messages.success(request,"Successfully Add Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
    except:
        messages.error(request,"Failed to Add Result")
        return HttpResponseRedirect(reverse("staff_add_result"))



def student_feedback_message(request):
    feedbacks=FeedbackStudent.objects.all()
    return render(request,"staff_template/student_feedback_template.html",{"feedbacks":feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")



def staff_view_result(request):
    student=StudentResult.objects.all()
    # studentresult=StudentResult.objects.filter(student_id=student.id)
    print(student)
    return render(request,"staff_template/hi.html",{"student":student})

