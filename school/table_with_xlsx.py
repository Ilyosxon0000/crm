import openpyxl
from myconf.conf import get_model
from myconf import conf
from django.db import transaction

class AddLessonWithExcel:
    def __init__(self, file_path, sinf=None, kun=None, fan=None, teacher=None, vaqt=None, a={}, sinfi=None):
        self.file_path = file_path
        self.sinf = sinf
        self.kun = kun
        self.fan = fan
        self.teacher = teacher
        self.vaqt = vaqt
        self.a = a
        self.sinfi = sinfi

    @transaction.atomic
    def start(self):
        lessons = []
        re = openpyxl.load_workbook(self.file_path)
        s = re.sheetnames
        data = re[s[0]]

        sinf = [i.title for i in get_model(conf.CLASS).objects.all()]
        DAY_CHOICES = get_model(conf.LESSON).DAY_CHOICES

        kunlar = tuple([i[1] for i in DAY_CHOICES])
        kunlar_ = ('#', 'Vaqt', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba')

        li = []
        vaqtlar = []
        for x in data.values:
            if str(x[0]).isdigit() and len(vaqtlar) < 9:
                vaqtlar.append(x[1])

            if type(x[0]) == str and x[0].strip() in sinf:
                self.a = {}
                self.sinfi = x[0].strip()
                self.a[self.sinfi] = []
                for d in kunlar:
                    r = {}
                    fan = {}
                    teach = {}
                    r[d] = [fan, teach]
                    self.a[self.sinfi].append(r)
                continue

            if type(x[0]) == int:
                for f in range(2, len(x)):
                    if 'fanlar' in self.a[self.sinfi][f - 2][kunlar_[f]][0].keys():
                        self.a[self.sinfi][f - 2][kunlar_[f]][0]['fanlar'].append(x[f])
                    else:
                        self.a[self.sinfi][f - 2][kunlar_[f]][0]['fanlar'] = [x[f]]

            if any(x) and x[0] == x[1]:
                for f in range(2, len(x)):
                    if 'teachers' in self.a[self.sinfi][f - 2][kunlar_[f]][1].keys():
                        self.a[self.sinfi][f - 2][kunlar_[f]][1]['teachers'].append(x[f])
                    else:
                        self.a[self.sinfi][f - 2][kunlar_[f]][1]['teachers'] = [x[f]]
                    if f == len(x) and self.a[self.sinfi] == '11-self.a sinf':
                        break
            if x[0] == 9:
                li.append(self.a)

        lesson_times = get_model(conf.LESSON_TIME).objects.all()
        lesson_times.delete()

        vaqtlar_times = [str(vaqt).replace(" ", "").split("-") for vaqt in vaqtlar]
        for item in vaqtlar_times:
            get_model(conf.LESSON_TIME).objects.create(
                begin_time=item[0],
                end_time=item[1],
            )

        for x in li:
            sinf = list(x.keys())[0]
            for i in x[sinf]:
                kun = list(i.keys())[0]
                for y, b in zip(i[kun][0].values(), i[kun][1].values()):
                    s = 0
                    for fan, teacher in zip(y, b):
                        if 9 > s:
                            s += 1
                        else:
                            s = 0
                        lesson_time = get_model(conf.LESSON_TIME).objects.get(
                            begin_time=vaqtlar_times[s - 1][0],
                            end_time=vaqtlar_times[s - 1][1],
                        )
                        science = None
                        if fan:
                            science = get_model(conf.SCIENCE).objects.get_or_create(title=fan)[0]
                        student_class = get_model(conf.CLASS).objects.get(title=sinf)
                        get_model(conf.LESSON).objects.create(
                            teacher=teacher,
                            science=science,
                            student_class=student_class,
                            lesson_date=kun,
                            lesson_time=lesson_time,
                        )
