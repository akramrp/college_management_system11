from django.core.files.storage import FileSystemStorage
from college_management_app.models import Course, CustomUser, SessionYearModel
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from college_management_app.EmailBackEnd import EmailBackEnd
import json


# Create your views here.
def showDemoPage(request):
    return HttpResponse('hello demo page')


def showLoginPage(request):
    return render(request, 'login_page.html')


def doLogin(request):
    # return HttpResponse(request.POST.get('email')+', '+request.POST.get('password'))
    if request.method != 'POST':
        return HttpResponse('<h2>Method Not Allowed</h2>')
    else:
        # captcha_token = request.POST.get("g-recaptcha-response")
        # cap_url = "https://www.google.com/recaptcha/api/siteverify"
        # cap_secret = "6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data = {"secret": cap_secret, "response": captcha_token}
        # cap_server_response = requests.post(url=cap_url, data=cap_data)
        # cap_json = json.loads(cap_server_response.text)
        #
        # if cap_json['success'] == False:
        #     messages.error(request, "Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")

        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse('staff_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))
        else:
            messages.error(request, "Invalid Login Details!!")
            return HttpResponseRedirect('/')


def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "YOUR_API_KEY",' \
         '        authDomain: "FIREBASE_AUTH_URL",' \
         '        databaseURL: "FIREBASE_DATABASE_URL",' \
         '        projectId: "FIREBASE_PROJECT_ID",' \
         '        storageBucket: "FIREBASE_STORAGE_BUCKET_URL",' \
         '        messagingSenderId: "FIREBASE_SENDER_ID",' \
         '        appId: "FIREBASE_APP_ID",' \
         '        measurementId: "FIREBASE_MEASUREMENT_ID"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'
    return HttpResponse(data,content_type="text/javascript")
    

def signup_admin(request):
    return render(request, 'signup_admin_page.html')


def do_admin_signup(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed')
        return HttpResponseRedirect(reverse('signup_admin'))
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=1)
            user.save()
            messages.success(request, "Successfully Admin Created")
            return HttpResponseRedirect(reverse('show_login'))
        except:
            messages.error(request, "Failed To Create Admin")
            return HttpResponseRedirect(reverse('signup_admin'))



def signup_staff(request):
    return render(request, 'signup_staff_page.html')


def do_staff_signup(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed')
        return HttpResponseRedirect(reverse('signup_staff'))
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Staff Created")
            return HttpResponseRedirect(reverse('show_login'))
        except:
            messages.error(request, "Failed To Create Staff")
            return HttpResponseRedirect(reverse('signup_staff'))


def signup_student(request):
    courses = Course.objects.all()
    session_years = SessionYearModel.objects.all()
    return render(request, 'signup_student_page.html', {"courses":courses, "session_years":session_years})


def do_student_signup(request):
    if request.method != 'POST':
        messages.error(request, 'Method Not Allowed')
        return HttpResponseRedirect(reverse('signup_student'))
    else:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        course_id = request.POST.get('course')
        gender = request.POST.get('gender')
        session_year_id = request.POST.get('session_year')
        profile_pic = request.FILES.get('profile_pic')

        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, user_type=3)
            user.students.gender = gender
            user.students.address = address
            course_obj = Course.objects.get(id=course_id)
            user.students.course_id = course_obj
            session_obj = SessionYearModel.objects.get(id=session_year_id)
            user.students.session_year_id = session_obj
            user.students.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Successfully Student Created")
            return HttpResponseRedirect(reverse('show_login'))
        except:
            messages.error(request, "Failed To Student Staff")
            return HttpResponseRedirect(reverse('signup_student'))