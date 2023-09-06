import datetime
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
# school app models
SCIENCE="school.Science"#Fanlar modeli
CLASS="school.Class"#Sinf modeli

# accounts app models
TEACHER="accounts.Teacher"#Teacher modeli
EMPLOYER="accounts.Employer"#Xodim modeli
STUDENT="accounts.Student"#Xodim modeli