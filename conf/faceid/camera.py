from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .face_rec import FaceRecognition
from rest_framework.decorators import api_view
from myconf.conf import get_model
from myconf import conf
from datetime import datetime
from django.utils import timezone

def cam_entrance(request,users):
    camera=get_model(conf.COMPANY).objects.all()
    camera=camera[0].camera_entrance if camera else None
    if camera:
        try:
            response=0
            cam1=FaceRecognition(users=users,similarity=0.5,limit=5)
            result=cam1.start(camera=camera)
            print("result:",result)
            if 'result' in result:
                if result['result']:
                    message=result['message']
                    user=get_user_model().objects.get(id=message['id'])
                    attendance=get_model(conf.ATTENDANCE).objects.get_or_create(
                        user=user,
                        date=datetime.now().date()
                    )[0]
                    attendance.attendance_type=get_model(conf.ATTENDANCE).KELGAN
                    attendance.date_enter=timezone.now()
                    attendance.save()

                    # TODO SMS PARENT
                    response=1
            cam1.stop()
            return {"message":response}
        except AttributeError:
            cam1.stop()
            return {"message":0}
    return {"message":0}

def cam_exit(request,users):
    camera=get_model(conf.COMPANY).objects.filter(active=True)[0].camera_exit
    camera=get_model(conf.COMPANY).objects.filter(active=True)
    camera=camera[0].camera_entrance if camera else None
    if camera:
        try:
            response=0
            cam1=FaceRecognition(users=users,similarity=0.5,limit=5)
            result=cam1.start(camera=camera)
            if 'result' in result:
                if result['result']:
                    message=result['message']
                    user=get_user_model().objects.get(id=message['id'])
                    attendance=get_model(conf.ATTENDANCE).objects.get_or_create(
                        user=user,
                        date=datetime.now().date()
                    )[0]
                    attendance.date_leave=timezone.now()
                    attendance.save()
                    # TODO SMS PARENT
                    response=1
            cam1.stop()
            return {"message":response}
        except AttributeError:
            cam1.stop()
            return {"message":0}
    return {"message":0}

@api_view(['GET'])
def cam(request,pk):
    users=get_user_model().objects.filter(is_active=True)
    users_list=[]
    for user in users:
        if user.image:
            user_dict={
                "id":user.id,
                "username":user.get_username(),
                "path":user.image.path
            }
            users_list.append(user_dict)
    response_data = {"message":0}
    if pk == 1 and users_list:
        response_data = cam_entrance(request, users=users_list)
    elif pk == 2 and users_list:
        response_data = cam_exit(request, users=users_list)

    return JsonResponse(response_data,safe=True)


