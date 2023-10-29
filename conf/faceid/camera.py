from django.http import JsonResponse
from django.contrib.auth import get_user_model
from . import face_rec
from rest_framework.decorators import api_view
from myconf.conf import get_model
from myconf import conf
from datetime import datetime
def cam_entrance(request,users):
    camera=get_model(conf.COMPANY).objects.filter(active=True)[0].camera_entrance
    try:
        response=0
        cam1=face_rec.FaceRecognition(users=users,similarity=0.5,limit=5)
        result=cam1.start(camera=camera)
        print(result)
        if 'result' in result:
            if result['result']:
                message=result['message']
                user=get_user_model.objects.get(id=message['id'])
                attendance=get_model(conf.ATTENDANCE).objects.get(
                    user=user,
                    date__year=datetime.now().year,
                    date__month=datetime.now().month,
                    date__day=datetime.now().day
                )
                attendance.attendance_type=get_model(conf.ATTENDANCE).KELGAN
                attendance.date=datetime.now()
                attendance.save()
                # TODO SMS PARENT
                response=1
        cam1.stop()
        return {"message":response}
    except AttributeError:
        cam1.stop()
        return {"message":0}

def cam_exit(request,users):
    camera=get_model(conf.COMPANY).objects.filter(active=True)[0].camera_exit
    try:
        response=0
        cam1=face_rec.FaceRecognition(users=users,similarity=0.5,limit=5)
        result=cam1.start(camera=camera)
        if 'result' in result:
            if result['result']:
                message=result['message']
                user=get_user_model.objects.get(id=message['id'])
                attendance=get_model(conf.ATTENDANCE).objects.get(
                    user=user,
                    date__year=datetime.now().year,
                    date__month=datetime.now().month,
                    date__day=datetime.now().day
                )
                attendance.date_leave=datetime.now()
                attendance.save()
                # TODO SMS PARENT
                response=1
        cam1.stop()
        return {"message":response}
    except AttributeError:
        cam1.stop()
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
    response_data = None
    if pk == 1:
        response_data = cam_entrance(request, users=users_list)
    elif pk == 2:
        response_data = cam_exit(request, users=users_list)

    return JsonResponse(response_data)


