## How To Setup Django On Linux
    1. sudo apt-get update && sudo apt-get -y upgrade
    2. sudo apt-get install python3
    3. python3 -V
    4. sudo apt-get install -y python3-pip
    5. pip3 -V
    6. pip3 install virtualenv
    7. virtualenv --version
    8. virtualenv cenv
    9. . cenv/bin/activate  |  source cenv/bin/activate
    10. pip3 install django
    11. django-admin --version
    12. pip3 install mysql-connector-python
    13. sudo apt-get install python-dev default-libmysqlclient-dev
    14. pip3 install mysqlclient
    15. pip3 freeze > requirements.txt | pip3 install -r requirements.txt
    16. python3 manage.py migrate
    17. python3 manage.py createsuperuser
    18. python3 manage.py runserve


## start coding....
    sex_choice = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
    sex = models.CharField(max_length=50, choices=sex_choice, default='Male')

## reference link:
    forgot password process: 
        https://learndjango.com/tutorials/django-password-reset-tutorial
    
    all django template tag and filter:
        https://www.djangotemplatetagsandfilters.com/



-------------------pending-----------------
1. watch db design video again
2. # same model only one field difference
    FeedbackStudent | FeedbackStaff
    LeaveReportStudent | LeaveReportStaff
    NotificationStudent | NotificationStaffs
3. rechack -> login process
4. password_reset apply link in login page
5. capcha code validatation
6. confirm again home_content.html

7. staff:
    confirm again staff_content.html
    FeedbackStaff Model change student_id To Staff_id
    edit_student_result url not working staff
8. rest_frameworks
9. session and download pdf
10. change django admin.py
11.  live with heroku