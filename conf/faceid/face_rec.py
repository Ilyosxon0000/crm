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
        self.limit1=limit
        self.limit2=limit
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
                    current_faces=[]
                    if len(faces):
                        for face in faces:
                            frame_embedding = face.embedding
                            x, y, w, h = face.bbox.astype(int)
                            # print(face)
                            # un_face={
                            #     "x":x,
                            #     "y":y,
                            #     "w":w,
                            #     "h":h,
                            #     "face":frame_embedding
                            # }
                            # current_faces.append(un_face)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                            for user in range(len(self.users)):
                                src=self.users[user]
                                src_image = cv2.imread(src['path'])
                                src_faces = self.model.get(src_image)
                                if len(src_faces):
                                    src_face = src_faces[0]
                                    src_embedding = src_face.embedding
                                else:
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
                                    if user+1==len(self.users) and self.limit1==0:
                                        return {"message":"Not known"}
                                    self.limit1-=1
                                else:
                                    return {"message":"src_embedding is None"}
                        # print("current_faces:",current_faces) # TODO face if len(face)>1
                    elif len(faces)==False and self.limit2==0:
                        return {"message":"face hasn't"}
                    self.limit2-=1
            except KeyboardInterrupt:
                pass
            finally:
                vs.stop()
        return {"message":"camera is offline"}
    
    def stop(self):
        self.running=False
