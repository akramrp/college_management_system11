import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
# import requests
from college_management_app.forms import AddStudentForm
from college_management_app.models import Attendance, AttendanceReport, CustomUser, NotificationStaffs, NotificationStudent, Staffs, Course, Subjects, SessionYearModel, Students, FeedbackStudent, FeedbackStaff, LeaveReportStudent, LeaveReportStaff


def admin_home(request):
    student_count1 = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Course.objects.all().count()

    course_all = Course.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course = Course.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    staffs = Staffs.objects.all()
    attendance_present_list_staff = []
    attendance_absent_list_staff = []
    staff_name_list = []
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        attendance=Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        attendance_present_list_staff.append(attendance)
        attendance_absent_list_staff.append(leaves)
        staff_name_list.append(staff.admin.username)

    students_all=Students.objects.all()
    attendance_present_list_student=[]
    attendance_absent_list_student=[]
    student_name_list=[]
    for student in students_all:
        attendance=AttendanceReport.objects.filter(student_id=student.id,status=True).count()
        absent=AttendanceReport.objects.filter(student_id=student.id,status=False).count()
        leaves=LeaveReportStudent.objects.filter(student_id=student.id,leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves+absent)
        student_name_list.append(student.admin.username)

    return render(request,"hod_template/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,"course_name_list":course_name_list,"subject_count_list":subject_count_list,"student_count_list_in_course":student_count_list_in_course,"student_count_list_in_subject":student_count_list_in_subject,"subject_list":subject_list,"staff_name_list":staff_name_list,"attendance_present_list_staff":attendance_present_list_staff,"attendance_absent_list_staff":attendance_absent_list_staff,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})

    # return render(request, "hod_template/home_content.html",
    #               {"student_count": 22, "staff_count": 23, "subject_count": 34,
    #                "course_count": 45, "course_name_list": 55,
    #                "subject_count_list": 66,"student_count_list_in_course": 77,
    #                "student_count_list_in_subject": 88, "subject_list": 99,
    #                "staff_name_list": 12, "attendance_present_list_staff": 14,
    #                "attendance_absent_list_staff": 44, "student_name_list": 35,
    #                "attendance_present_list_student": 33,
    #                "attendance_absent_list_student": 27})


def add_staff(request):
    return render(request, 'hod_template/add_staff.html')


def add_staff_save(request):
    if request.method != 'POST':
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse("add_staff"))
    else:
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        address = request.POST['address']
        # print(email+password+first_name+last_name)
        try:
            user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name,
                                                  last_name=last_name, email=email, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully! Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed To Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff.html",{"staff": staff, "id": staff_id})


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST['staff_id']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        address = request.POST['address']
        
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()
            
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Successfully! Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id":staff_id}))
        except:
            messages.error(request, "Failed To Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id":staff_id}))

def add_course(request):
    return render(request, 'hod_template/add_course.html')


def add_course_save(request):
    if request.method != 'POST':
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse("add_course"))
    else:
        course_name = request.POST.get('course_name1')
        try:
            course_model = Course(course_name=course_name)
            course_model.save()
            messages.success(request, "Successfully! Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except Exception as error:
            # print(error)
            messages.error(request, "Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request,"hod_template/edit_course.html",{"course": course, "course_id": course_id})


def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST['course_id']
        course_name = request.POST['course_name']
        
        try:
            course_model = Course.objects.get(id=course_id)
            course_model.course_name = course_name
            course_model.save()

            messages.success(request, "Successfully! Edited Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))
        except:
            messages.error(request, "Failed To Edit Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))


def add_subject(request):
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_template/add_subject.html', {"courses": courses,"staffs": staffs})


def add_subject_save(request):
    if request.method != 'POST':
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse("add_subject"))
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Course.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject.html",{"subject":subject, "staffs":staffs, "courses":courses,"subject_id":subject_id})


def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Course.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def add_student(request):
    form = AddStudentForm()
    return render(request, 'hod_template/add_student.html', {"form": form})


def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse("add_student"))
    else:
        form = AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            gender = form.cleaned_data["gender"]

            profile_pic = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            # print("profile_pic", profile_pic)
            # print("profile_pic_url", profile_pic_url)
            # print(first_name, last_name, username, email, password, address, session_year_id, course_id, gender); pass

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=3)
                user.students.gender = gender
                user.students.address = address
                course_obj = Course.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "hod_template/add_student.html", {"form": form})


def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student.html', {"students": students})


def edit_student(request, student_id):
    return HttpResponse('hello edit_student ')


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_template/manage_staff.html', {"staffs": staffs})


def manage_course(request):
    courses = Course.objects.all()
    return render(request,'hod_template/manage_course.html', {"courses": courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_template/manage_subject.html", {"subjects": subjects})


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'hod_template/admin_profile.html', {"user": user})

def admin_profile_save(request):
    if request.method != 'POST':
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse('admin_profile'))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            user_model = CustomUser.objects.get(id=request.user.id)
            user_model.first_name = first_name
            user_model.last_name = last_name
            if password !='' and password != None:
                user_model.password = password
            user_model.save()
            messages.success(request, "Successfully! Update Profile Details")
            return HttpResponseRedirect(reverse('admin_profile'))
        except:
            messages.error(request, "Failed! To Update Profile Details")
            return HttpResponseRedirect(reverse('admin_profile'))


def manage_session(request):
    date = datetime.date.today()
    sessions = SessionYearModel.objects.all()
    return render(request, 'hod_template/manage_session.html', {'date': date, "sessions": sessions})


def add_session_save(request):
    if request.method != 'POST':
        messages.error(request, "Method Not Allowed!")
        return HttpResponseRedirect(reverse('manage_session'))
    else:
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        try:
            session_model = SessionYearModel(session_start_year=session_start, session_end_year=session_end)
            session_model.save()
            messages.success(request, "Successfully! Added Session Year")
            return HttpResponseRedirect(reverse('manage_session'))
        except:
            messages.error(request, "Failed! To Add Session Year")
            return HttpResponseRedirect(reverse('manage_session'))


def student_feedback_message(request):
    feedbacks = FeedbackStudent.objects.all()
    return render(request, 'hod_template/student_feedback.html', {"feedbacks": feedbacks})


def staff_feedback_message(request):
    feedbacks = FeedbackStaff.objects.all()
    return render(request, 'hod_template/staff_feedback.html', {"feedbacks": feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request, "hod_template/student_leave_view.html", {"leaves": leaves})


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))

def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request, "hod_template/staff_leave_view.html", {"leaves": leaves})


def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_disapprove_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    return render(request, "hod_template/admin_view_attendance.html", {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST['subject']
    session_year_id = request.POST['session_year_id']
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), content_type="application/json", safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST['attendance_date']
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    student_list_data = []
    for student in attendance_data:
        student_data={"id":student.student_id.admin.id, "name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name, "status":student.status}
        student_list_data.append(student_data)
    return JsonResponse(json.dumps(student_list_data), content_type="application/json", safe=False)


def admin_send_notification_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_template/staff_notification.html', {"staffs": staffs})


def admin_send_notification_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/student_notification.html', {"students": students})


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def send_student_notification(request):
    pass
    # id = request.POST.get("id")
    # message = request.POST.get("message")
    # student = Students.objects.get(admin=id)
    # token = student.fcm_token
    # url = "https://fcm.googleapis.com/fcm/send"
    # body = {
    #     "notification":{
    #         "title":"Student Management System",
    #         "body":message,
    #         "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
    #         "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
    #     },
    #     "to":token
    # }
    # headers = {"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    # data = requests.post(url,data=json.dumps(body),headers=headers)
    # notification = NotificationStudent(student_id=student,message=message)
    # notification.save()
    # print(data.text)
    # return HttpResponse("True")


@csrf_exempt
def send_staff_notification(request):
    pass
    # id = request.POST['id']
    # message = request.POST['message']
    # staff = Staffs.objects.get(admin=id)
    # token = staff.fcm_token
    # url="https://fcm.googleapis.com/fcm/send"
    # body={
    #     "notification":{
    #         "title":"Student Management System",
    #         "body":message,
    #         "click_action":"https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
    #         "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
    #     },
    #     "to":token
    # }
    # headers = {"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    # data = requests.post(url,data=json.dumps(body),headers=headers)
    # notification = NotificationStaffs(staff_id=staff,message=message)
    # notification.save()
    # print(data.text)
    # return HttpResponse("True")