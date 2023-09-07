import datetime
from django.contrib.auth import get_user_model
from django.apps import apps

def get_model(Model):
    model_class = apps.get_model(Model, require_ready=False)
    return model_class
# global func
def get_date(types):
    current_date = datetime.datetime.now()
    # formatted_date = current_date.strftime("%Y_%m_%d")
    if types=="year":
        return current_date.year
    elif types=="month":
        return current_date.month
    elif types=="week":
        return current_date.isocalendar()[1]
    elif types=="week_day":
        return current_date.weekday
    elif types=="day":
        return current_date.day
    elif types=="current_date":
        return current_date

# accounts app models
TYPE_OF_ADMIN="accounts.Type_of_Admin"#Teacher modeli
PERMISSION="accounts.Permission"#Teacher modeli
ADMIN="accounts.ADMIN"#Teacher modeli
TEACHER="accounts.Teacher"#Teacher modeli
EMPLOYER="accounts.Employer"#Xodim modeli
STUDENT="accounts.Student"#Xodim modeli
PARENT="accounts.Parent"#Xodim modeli

# school app models
SCIENCE="school.Science"#Fanlar modeli
CLASS="school.Class"#Sinf modeli
ATTENDANCE="school.Attendance"#Davomat modeli
ROOM="school.Room"#Davomat modeli
LESSON_TIME="school.Lesson_Time"#Dars soati modeli
LESSON="school.Lesson"#Davomat modeli
GRADE="school.Grade"#Davomat modeli

# finance app models
FINANCE="finance.Finance"
STUDENT_PAY="finance.Student_Pay"
