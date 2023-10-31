import insightface
import cv2
from imutils.video import VideoStream
from sklearn.metrics.pairwise import cosine_similarity

model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=0)
src="http://192.168.1.143:4747/video"
vs = VideoStream(src=src).start()
try:
    while True:
        frame = vs.read()
        faces = model.get(frame)
        if len(faces):
            for face in faces:
                frame_embedding = face.embedding
                x, y, w, h = face.bbox.astype(int)
                cv2.rectangle(frame, (x, y), (x + round(w/2.1), y + round(h/1.7)), (0, 255, 0), 2)
                sources=[
                        {
                            "username":"AbdulHamidxon",
                            "path":"/home/ilyosxon/dev/face-recognition/1-dars/media/src/AbdulHamidxon.jpg"
                        },
                        {
                            "username":"Ilyosxon",
                            "path":"/home/ilyosxon/dev/face-recognition/1-dars/media/src/Ilyosxon.JPG"
                        },
                    ]
                for src in sources:
                    print(src['username'])
                    src_image = cv2.imread(src['path'])
                    src_faces = model.get(src_image)
                    if len(src_faces):
                        src_face = src_faces[0]
                        src_embedding = src_face.embedding
                    else:
                        print("No face detected in the source image")
                        src_embedding = None

                    if src_embedding is not None:
                        similarity = cosine_similarity([src_embedding], [frame_embedding])[0][0]
                        if similarity > 0.5:
                            text_position = (x, y - 10)
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            font_scale = 0.5
                            font_color = (0, 0, 255)
                            font_thickness = 1
                            cv2.putText(frame, src['username'], text_position, font, font_scale, font_color, font_thickness)
                            cv2.imwrite("./output.jpg", frame)
                            import sys,time
                            time.sleep(1)
                            sys.exit("Exiting program")

finally:
    vs.stop()
