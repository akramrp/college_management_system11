import datetime
from django.contrib import messages
from django.http import request
from django.urls.base import reverse
from django.views.decorators.csrf import csrf_exempt
from college_management_app.models import Attendance, AttendanceReport, Course, CustomUser, FeedbackStudent, LeaveReportStudent, NotificationStudent, OnlineClassRoom, SessionYearModel, StudentResult, Students, Subjects
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    course = Course.objects.get(id=student_obj.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()
    subjects_data = Subjects.objects.filter(course_id=course)
    session_obj = SessionYearModel.objects.get(id=student_obj.session_year_id.id)
    class_room = OnlineClassRoom.objects.filter(subject__in=subjects_data, is_active=True, session_year=session_obj)

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request,"student_template/student_home.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent,"class_room":class_room})


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, 'student_template/student_view_attendance.html',{"subjects":subjects} )

def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request, 'student_template/student_profile.html', {"user": user, "student":student})

def student_profile_save(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed')
        return HttpResponseRedirect(reverse('student_profile'))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            custom_user_obj = CustomUser.objects.get(id=request.user.id) 
            custom_user_obj.first_name = first_name
            custom_user_obj.last_name = last_name
            if password != None and password !='':
                custom_user_obj.set_password(password)
            custom_user_obj.save()

            student_obj = Students.objects.get(admin=custom_user_obj)
            student_obj.address = address
            student_obj.save()

            messages.success(request, 'Successfully Updated Profile')
            return HttpResponseRedirect(reverse('student_profile'))
        except:
            messages.error(request, 'Failed to Update Profile')
            return HttpResponseRedirect(reverse('student_profile'))


def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request, 'student_template/student_apply_leave.html', {"leave_data":leave_data})


def student_apply_leave_save(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed')
        return HttpResponseRedirect(reverse('student_apply_leave'))
    else:
        try:
            leave_date = request.POST.get('leave_date')
            leave_message = request.POST.get('leave_message')
            student_obj = Students.objects.get(admin=request.user.id)

            leave_obj = LeaveReportStudent(student_id=student_obj, leave_date=leave_date, leave_message=leave_message, leave_status=0) 
            leave_obj.save()
            messages.success(request, 'Successfully Applied For Leave')
            return HttpResponseRedirect(reverse('student_apply_leave'))
        except:
            messages.error(request, 'Failed to Apply For Leave')
            return HttpResponseRedirect(reverse('student_apply_leave'))


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id=student_obj)
    return render(request, 'student_template/student_feedback.html', {"feedback_data":feedback_data})


def student_feedback_save(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed')
        return HttpResponseRedirect(reverse('student_feedback'))
    else:
        try:
            feedback = request.POST.get("feedback")
            student_obj = Students.objects.get(admin=request.user.id)
            feedeback_obj = FeedbackStudent(student_id=student_obj, feedback=feedback, feedback_reply='') 
            feedeback_obj.save()
            messages.success(request, 'Successfully Applied Feedback')
            return HttpResponseRedirect(reverse('student_feedback'))
        except:
            messages.error(request, 'Failed to Apply Feedback')
            return HttpResponseRedirect(reverse('student_feedback'))


def student_view_result(request):
    student_obj = Students.objects.get(admin=request.user.id)
    results = StudentResult.objects.filter(student_id=student_obj)
    return render(request, 'student_template/student_view_result.html', {"results":results})


def student_all_notification(request):
    student_obj = Students.objects.get(admin=request.user.id)
    notifications = NotificationStudent.objects.filter(student_id=student_obj)
    return render(request, 'student_template/student_all_notification.html', {"notifications":notifications})


def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_data_parse = datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=subject_id)
    user_object = CustomUser.objects.get(id=request.user.id)
    stud_obj = Students.objects.get(admin=user_object)

    attendance = Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)
    return render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})

def join_class_room(request, subject_id, session_year_id):
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    subjects=Subjects.objects.filter(id=subject_id)
    if subjects.exists():
        session=SessionYearModel.object.filter(id=session_year_obj.id)
        if session.exists():
            subject_obj=Subjects.objects.get(id=subject_id)
            course=Course.objects.get(id=subject_obj.course_id.id)
            check_course=Students.objects.filter(admin=request.user.id,course_id=course.id)
            if check_course.exists():
                session_check=Students.objects.filter(admin=request.user.id,session_year_id=session_year_obj.id)
                if session_check.exists():
                    onlineclass=OnlineClassRoom.objects.get(session_years=session_year_id,subject=subject_id)
                    return render(request,"student_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

                else:
                    return HttpResponse("This Online Session is Not For You")
            else:
                return HttpResponse("This Subject is Not For You")
        else:
            return HttpResponse("Session Year Not Found")
    else:
        return HttpResponse("Subject Not Found")



@csrf_exempt
def student_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        student = Students.objects.get(admin=request.user.id)
        student.fcm_token = token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")