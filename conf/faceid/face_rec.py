import insightface
import cv2
from imutils.video import VideoStream
from sklearn.metrics.pairwise import cosine_similarity
class FaceRecognition:
    def __init__(self,users,similarity,limit):
        self.model=None
        self.users=users
        self.similarity=similarity
        self.running = True
        self.limit=limit
    def check_camera(self,camera):
        try:
            cap = cv2.VideoCapture(camera)
            if not cap.isOpened():
                return False
            else:
                cap.release()
                return True
        except cv2.error as e:
            return False

    def start(self,camera):
        camera_is_online=self.check_camera(camera)
        if camera_is_online:
            try:
                self.model=insightface.app.FaceAnalysis()
                self.model.prepare(ctx_id=0,det_size=(640,640))
                vs = VideoStream(src=camera).start()
                while self.running:
                    frame = vs.read()
                    faces = self.model.get(frame)
                    if len(faces):
                        for face in faces:
                            frame_embedding = face.embedding
                            x, y, w, h = face.bbox.astype(int)
                            print(w,h)#TODO Eng katta faceni aniqlash
                            cv2.rectangle(frame, (x, y), (x + round(w/2.1), y + round(h/1.7)), (0, 255, 0), 2)

                            for user in range(len(self.users)):
                                src=self.users[user]
                                src_image = cv2.imread(src['path'])
                                src_faces = self.model.get(src_image)
                                if len(src_faces):
                                    src_face = src_faces[0]
                                    src_embedding = src_face.embedding
                                else:
                                    print("No face detected in the source image")
                                    src_embedding = None
                                if src_embedding is not None:
                                    similarity = cosine_similarity([src_embedding], [frame_embedding])[0][0]
                                    if similarity > self.similarity:
                                        text_position = (x, y - 10)
                                        font = cv2.FONT_HERSHEY_SIMPLEX
                                        font_scale = 0.5
                                        font_color = (0, 0, 255)
                                        font_thickness = 1
                                        cv2.putText(frame, src['username'], text_position, font, font_scale, font_color, font_thickness)
                                        cv2.imwrite("./output.jpg", frame)
                                        return {"message":src,"result":True}
                                    elif user+1==len(self.users) and self.limit==0:
                                        return None
                                    self.limit-=1
                                else:
                                    return {"message":"src_embedding is None"}
                    elif len(faces)>1 and self.limit==0:
                        return None
                    self.limit-=1
            except KeyboardInterrupt:
                pass
            finally:
                vs.stop()
        return {"message":"camera is offline"}
    
    def stop(self):
        self.running=False
