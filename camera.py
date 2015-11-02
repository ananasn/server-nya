import cv2
import base64

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(300, 250)

    def get_encode_frame(self):
            ret, frame = self.cap.read()
            img = cv2.imencode('.jpg', frame)[1]
            return 'data:image/jpg;base64,'+ base64.encodestring(img)

    def destroy(self):
        self.cap.release()