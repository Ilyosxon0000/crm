from myconf.conf import get_model
from myconf import conf
from finance.models import Finance
from finance.serializers import FinanceSerializer
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from . import serializers
from django.db.models import F
from rest_framework.response import Response

# Create your views here.
class FinanceView(APIView):
    def get(self, request):

        all_fin = Finance.objects.all()
        # data=[]
        ser = FinanceSerializer(all_fin, many=True)
        # times = {
        #     "years":[],
        #     "months":[]
        # }
        # for i in all_fin:
        #     if i.date.year not in times["years"]:
        #         times['years'].append(i.date.year)
        #     if i.date.month not in times['months']:
        #         times['months'].append(i.date.month)  
        # year_fin = Finance.objects.filter(date__year=2023).aggregate(
        #     total = Sum('amount')
        # )
        # month_fin = Finance.objects.filter(date__month=9).aggregate(
        #     total = Sum('amount')
        # )
        # print(times)
        # dic = {
        #     'year': 2023,
        #     'kirim': 12000
        # }
        # print(year_fin)
        # print(month_fin)

        last_object=Finance.objects.latest('date')
        first_object=Finance.objects.earliest('date')
        print("first object year:",first_object.date.year)
        print("first object month:",first_object.date.month)
        print("first object day:",first_object.date.day)

        print("last object year:",last_object.date.year)
        print("last object month:",last_object.date.month)
        print("last object day:",last_object.date.day)

        return Response(ser.data)
# class FinanceView(ModelViewSet):
#     queryset=get_model(conf.FINANCE).objects.all()
#     serializer_class=serializers.FinanceSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         custom = self.request.GET.get("custom")
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         elif custom is not None:
#             return self.custom_list(self, request,*args, **kwargs)


#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     def custom_list(self,request,*args,**kwargs):
#         queryset_years = self.filter_queryset(self.get_queryset()).annotate(
#             year=F('date__year'),
#         ).order_by('year')
#         queryset_months = self.filter_queryset(self.get_queryset()).annotate(
#             year=F('date__year'),
#             month=F('date__month'),
#         ).order_by('year','month')
#         queryset_days = self.filter_queryset(self.get_queryset()).annotate(
#             year=F('date__year'),
#             month=F('date__month'),
#             day=F('date__day')
#         ).order_by('year','month','day')
#         serializer = self.get_serializer(queryset_days, many=True)
#         return Response(serializer.data)

# class FinanceView(ModelViewSet):
#     queryset = get_model(conf.FINANCE).objects.all()
#     serializer_class = serializers.FinanceSerializer

#     def list(self, request, *args, **kwargs):
#         custom = self.request.GET.get("custom")
#         page = self.paginate_queryset(self.queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         elif custom is not None:
#             return self.custom_list(request, *args, **kwargs)

#         serializer = self.get_serializer(self.queryset, many=True)
#         return Response(serializer.data)

#     def custom_list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.queryset).annotate(
#             year=F('date__year'),
#             month=F('date__month'),
#             day=F('date__day'),
#         ).order_by('year', 'month', 'day')

#         data = {}
#         for item in queryset:
#             year = item.get('year')
#             month = item.get('month')
#             day = item.get('day')
#             amount = item.get('amount')
#             types_finance = item.get('types_finance')

#             # Create a dictionary structure to organize the data
#             if year not in data:
#                 data[year] = {
#                     'date': item['date'],
#                     'months': {},
#                 }
#             if month not in data[year]['months']:
#                 data[year]['months'][month] = {
#                     'date': item['date'],
#                     'days': [],
#                 }
#             data[year]['months'][month]['days'].append({
#                 'date': item['date'],
#                 'amount': amount if types_finance == 'INCOME' else None,
#                 'kirim': amount if types_finance == 'INCOME' else None,
#                 'chiqim': amount if types_finance == 'EXPENSE' else None,
#             })

#         serialized_data = serializers.YearSerializer(data.values(), many=True)
#         return Response(serialized_data.data)

# class FinanceView(ModelViewSet):
#     queryset = get_model(conf.FINANCE).objects.all()
#     serializer_class = serializers.FinanceSerializer

#     def list(self, request, *args, **kwargs):
#         custom = self.request.GET.get("custom")
#         page = self.paginate_queryset(self.queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         elif custom is not None:
#             return self.custom_list(request, *args, **kwargs)

#         serializer = self.get_serializer(self.queryset, many=True)
#         return Response(serializer.data)

#     def custom_list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.queryset).annotate(
#             year=F('date__year'),
#             month=F('date__month'),
#             day=F('date__day'),
#         ).order_by('year', 'month', 'day')

#         data = []

#         for item in queryset:
#             year = item.year
#             month = item.month
#             day = item.day
#             amount = item.amount
#             types_finance = item.types_finance

#             # Check if the year already exists in data
#             year_exists = any(d['name'] == year for d in data)
#             if not year_exists:
#                 data.append({
#                     "name": year,
#                     "kirim": 0,
#                     "chiqim": 0,
#                     "months": [],
#                 })

#             # Find the index of the year in data
#             year_index = next((i for i, d in enumerate(data) if d['name'] == year), None)

#             # Check if the month already exists in data
#             month_exists = any(m['name'] == month for m in data[year_index]['months'])
#             if not month_exists:
#                 data[year_index]['months'].append({
#                     "name": month,
#                     "kirim": 0,
#                     "chiqim": 0,
#                     "days": [],
#                 })

#             # Find the index of the month in data
#             month_index = next((i for i, m in enumerate(data[year_index]['months']) if m['name'] == month), None)

#             # Add data for the day
#             data[year_index]['months'][month_index]['days'].append({
#                 "name": day,
#                 "kirim": amount if types_finance == 'INCOME' else 0,
#                 "chiqim": amount if types_finance == 'EXPENSE' else 0,
#             })

#             # Update kirim and chiqim totals
#             data[year_index]['kirim'] += amount if types_finance == 'INCOME' else 0
#             data[year_index]['chiqim'] += amount if types_finance == 'EXPENSE' else 0

#         # Assign the date to the first day of each month
#         for year_data in data:
#             for month_data in year_data['months']:
#                 month_data['date'] = f"{year_data['name']}-{month_data['name']:02d}-01"

#         return Response(data)



class Student_PayView(ModelViewSet):
    queryset=get_model(conf.STUDENT_PAY).objects.all()
    serializer_class=serializers.Student_PaySerializer

class Each_payView(ModelViewSet):
    queryset = get_model(conf.EACH_PAY).objects.all()
    serializer_class = serializers.Each_paySerializer