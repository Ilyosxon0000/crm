import insightface
import cv2
from imutils.video import VideoStream
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np,faiss
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
                        i=0
                        for face in faces:
                            frame_embedding = face.embedding
                            x, y, w, h = face.bbox.astype(int)
                            # print(face)
                            un_face={
                                "x":x,
                                "y":y,
                                "w":w,
                                "h":h,
                                # "face":frame_embedding
                            }
                            # current_faces.append({f"user {i}":un_face})
                            current_faces.append(face)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            text_position = (x, y - 10)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            font_scale = 0.5
                            font_color = (0, 0, 255)
                            font_thickness = 1
                            cv2.putText(frame, f"user {i}", text_position, font, font_scale, font_color, font_thickness)
                            cv2.imwrite("./output.jpg", frame)
                            i+=1
                    self.limit2-=1
                    print(current_faces)
                    # current_faces = np.array(current_faces)
                    # index = faiss.IndexFlatL2(current_faces.shape[1])
                    # index.add(current_faces)
                    # print(index)
                    return {"message":False}
            except KeyboardInterrupt:
                pass
            finally:
                vs.stop()
        return {"message":"camera is offline"}
    
    def stop(self):
        self.running=False
