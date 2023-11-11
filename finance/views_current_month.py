from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from myconf.conf import get_model
from myconf import conf
from . import serializers
from . import filters
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class StudentDebtView(ModelViewSet):
    queryset=get_model(conf.STUDENT_DEBT).objects.all()
    serializer_class=serializers.StudentDebtSerializer
    filterset_fields="__all__"

class InComeView(ModelViewSet):
    queryset=get_model(conf.INCOME).objects.all()
    serializer_class=serializers.InComeSerializer

    def get_serializer_class(self):
        if self.request.method=="GET":
            return serializers.InComeGetSerializer
        return super().get_serializer_class()

class ExpenseView(ModelViewSet):
    queryset=get_model(conf.EXPENSE).objects.all()
    serializer_class=serializers.ExpenseSerializer
    filterset_class=filters.ExpenseFilter

class Data_Finance(APIView):
    def get(self,request):
        import calendar
        from django.db.models import Sum
        from .models import InCome,Expense
        if (len(InCome.objects.all()) and len(Expense.objects.all()))==False:
            return Response([])#TODO      from First Element to current month
        last_income=InCome.objects.latest('created_date')
        first_income=InCome.objects.earliest('created_date')
        last_expense=Expense.objects.latest('created_date')
        first_expense=Expense.objects.earliest('created_date')
        first_object=int(first_income.created_date.year) if int(first_income.created_date.year)<int(first_expense.created_date.year) else int(first_expense.created_date.year)
        last_object=int(last_income.created_date.year) if int(last_income.created_date.year)>int(last_expense.created_date.year) else int(last_expense.created_date.year)

        current_date=datetime.now()
        years=[i for i in range(first_object,last_object+1)]
        data = {}
        for year in range(len(years)):
            s=years[year]
            li = []
            for x in range(1, 13):
                if year+1==len(years) and x>current_date.month:
                    break
                a, m = calendar.monthrange(s, x)
                li.append(m)
            z = list(zip(range(1, 13), li))
            if year+1==len(years):
                z = list(zip(range(1, current_date.month+1), li))
            if s not in data.keys():
                data[s] = z
        
        data_for_frontend = []
        for x in data.keys():
            data_for_list = {}
            yillik_income = InCome.objects.filter(created_date__year=x)
            yillik_expense = Expense.objects.filter(created_date__year=x)
            y_i = yillik_income.aggregate(total_year=Sum('amount'))
            y_e = yillik_expense.aggregate(total_year=Sum('amount'))
            data_for_list['name']=x
            data_for_list['kirim'] = y_i['total_year'] if y_i['total_year'] else 0
            data_for_list['chiqim'] = y_e['total_year'] if y_e['total_year'] else 0
            data_for_list['months'] = []
            for i in data[x]:
                month_name = calendar.month_name[i[0]]
                month_income = yillik_income.filter(created_date__month=i[0])
                month_expense = yillik_expense.filter(created_date__month=i[0])
                if month_income or month_expense:
                    m_i = month_income.aggregate(total_month=Sum('amount'))
                    m_e = month_expense.aggregate(total_month=Sum('amount'))
                    data_each_month = {
                        "name":month_name,
                        "kirim":m_i['total_month'] if m_i['total_month'] else 0,
                        "chiqim":m_e['total_month'] if m_e['total_month'] else 0,
                        'days': []
                    }
                    # data_each_month[month_name] = f['total_month']
                    kunlar = []
                    for kun in range(1, i[1] + 1):
                        kun_data={}
                        kun_income = month_income.filter(created_date__day=kun).aggregate(total_kun=Sum('amount'))
                        kun_expense = month_expense.filter(created_date__day=kun).aggregate(total_kun=Sum('amount'))
                        if kun_income or kun_expense:
                            kun_income_value = kun_income['total_kun'] if kun_income['total_kun'] else 0
                            kun_expense_value = kun_expense['total_kun'] if kun_expense['total_kun'] else 0
                            kun_data['name'] = kun
                            kun_data['kirim'] = kun_income_value
                            kun_data['chiqim'] = kun_expense_value
                        else:
                            kun_data['name'] = kun
                            kun_data['kirim'] = 0
                            kun_data['chiqim'] = 0
                        kunlar.append(kun_data)
                    data_each_month['days'].append(kunlar)
                else:
                    # 2-usul
                    data_each_month = {
                        "name":month_name,
                        "kirim":0,
                        "chiqim":0,
                        'days': []
                    }
                    kunlar = []
                    for kun in range(1, i[1] + 1):
                        kun_data={}
                        kun_data['name'] = kun
                        kun_data['kirim'] = 0
                        kun_data["chiqim"]=0
                        kunlar.append(kun_data)
                    data_each_month['days'].append(kunlar)

                    # data_each_month = {month_name: {"days":i[1]}}
                data_for_list['months'].append(data_each_month)
            data_for_frontend.append(data_for_list)

        return Response(data_for_frontend)
