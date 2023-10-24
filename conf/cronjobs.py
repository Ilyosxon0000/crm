from rest_framework.decorators import api_view
from rest_framework.response import Response
from myconf import conf
from django.contrib.auth import get_user_model
from myconf.conf import get_model
from django.db.models import Q
from datetime import datetime

@api_view(['GET'])
def davomat_users(request):
    current_date = datetime.now().isoweekday()
    if current_date!=7:
        users=get_user_model().objects.filter(~Q(type_user="parent"))
        for user in users:
            get_model(conf.ATTENDANCE).objects.create(user=user)
    return Response({"message": "succesfully"})
