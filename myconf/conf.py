import datetime
from django.apps import apps
from django.contrib.auth import get_user_model

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
TASK="school.Task"#Task modeli
TASK_FOR_CLASS="school.TaskForClass"#Davomat modeli
PARENT_COMMENT="school.Parent_Comment"#Ota ona comment modeli
TEACHER_LESSON="school.Teacher_Lesson"#Davomat modeli
QUESTION="school.Question"#Davomat modeli
COMPANY="school.Company"#Davomat modeli

def all_days():
    import datetime
    current_year = datetime.datetime.now().year
    start_date = datetime.datetime(current_year, 1, 1)
    end_date = datetime.datetime(current_year, 12, 31)
    all_days_of_year = []
    current_date = start_date
    while current_date <= end_date:
        all_days_of_year.append(current_date)
        current_date += datetime.timedelta(days=1)
    return all_days_of_year
    
def get_type_name_field(model,types):
    fields=get_model(model)._meta.get_fields()
    file_fields = [field.name for field in fields if isinstance(field, types)]
    return file_fields

# Finance
STUDENT_DEBT="finance.Student_Debt"
INCOME="finance.InCome"
EXPENSE="finance.Expense"