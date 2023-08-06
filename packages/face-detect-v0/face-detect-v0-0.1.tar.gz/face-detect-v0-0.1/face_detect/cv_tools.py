import cv2
import dlib
import numpy as np


class FaceDetector:

    def __init__(self):
        self._detector = dlib.get_frontal_face_detector()

    def detectLargestFace(self, targetImage):
        h, w, _ = targetImage.shape

        if (h * w) >= (1024 * 1024):
            raise Exception("Image Dimension Error!: {} * {} px".format(h, w))
        else:
            print("Size of image: {} * {} px".format(h, w))

            gray = cv2.cvtColor(targetImage, cv2.COLOR_BGR2GRAY)
            faces = self._detector(gray)
            print("Number of faces detected: {}".format(len(faces)))

            large_frame = faces[
                np.argmax([((abs(face.top() - face.bottom())) * (abs(face.left() - face.right()))) for face in faces])]
            print("Size of largest face detected: {} * {} px".format(
                (abs(large_frame.top() - large_frame.bottom())), (abs(large_frame.left() - large_frame.right()))))

            crop_img = targetImage[large_frame.top():large_frame.bottom(), large_frame.left():large_frame.right()]

        return crop_img