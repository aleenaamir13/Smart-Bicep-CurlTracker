import cv2
import mediapipe as mp
import time
import math
import numpy as np

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

class poseDetector():
    def __init__(self,MaxPoses=1,detectionCon=0.5, presenceCon=0.5,trackCon=0.5):
        self.MaxPoses=MaxPoses
        self.detectionCon = detectionCon
        self.presenceCon=presenceCon
        self.trackCon = trackCon
        self.running_mode = VisionRunningMode.VIDEO
        self.options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='pose_landmarker_heavy.task'),
            num_poses=MaxPoses,
            min_pose_detection_confidence = detectionCon,
            min_pose_presence_confidence=presenceCon,
            min_tracking_confidence = trackCon,
            running_mode=self.running_mode
        )
        self.detector = PoseLandmarker.create_from_options(self.options)
        self.frame_id = 0

    def findPose(self, img, timestamp,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,data=imgRGB)
        self.results = self.detector.detect_for_video(mp_image,timestamp)
        return img

    def findPosition(self, img, draw=True):
        POSE_CONNECTIONS = [
            (11, 12),
            (11, 13), (13, 15),
            (12, 14), (14, 16),
            (15, 17), (15, 19), (15, 21),
            (16, 18), (16, 20), (16, 22),
            (11, 23), (12, 24),
            (23, 24),
            (23, 25), (25, 27),
            (24, 26), (26, 28),
            (27, 29), (29, 31),
            (28, 30), (30, 32),
            (27, 31), (28, 32)
        ]
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks[0]):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)
            for a, b in POSE_CONNECTIONS:
                x1, y1 = self.lmList[a][1], self.lmList[a][2]
                x2, y2 = self.lmList[b][1], self.lmList[b][2]
                if draw:
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        return self.lmList

    def findAngle(self, img, p1, p2, p3, draw=True):

        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Create vectors
        v1 = np.array([x1 - x2, y1 - y2])
        v2 = np.array([x3 - x2, y3 - y2])

        # Dot product formula
        dot = np.dot(v1, v2)
        mag1 = np.linalg.norm(v1)
        mag2 = np.linalg.norm(v2)

        # avoid division error
        if mag1 == 0 or mag2 == 0:
            return 0

        cos_angle = dot / (mag1 * mag2)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)

        angle = np.degrees(np.arccos(cos_angle))

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)

            cv2.circle(img, (x1, y1), 8, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 8, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 8, (0, 0, 255), cv2.FILLED)

            cv2.putText(img, str(int(angle)), (x2 - 50, y2),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle
def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        lmList = detector.findPosition(img,timestamp, draw=True)
        if len(lmList) != 0:
            print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()