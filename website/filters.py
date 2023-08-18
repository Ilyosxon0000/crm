from .models import Davomat
from django_filters.rest_framework import filterset
from django.forms import CheckboxInput

class DavomatFilter(filterset.FilterSet):
    class Meta:
        model = Davomat
        fields = ["user","davomat",'date']

    
    # def is_valid(self):
    #     print(self.request.GET['user'])
    #     return super().is_valid()
