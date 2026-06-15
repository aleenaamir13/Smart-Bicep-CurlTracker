import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("curls.mp4")
detector = pm.poseDetector()

left_count = 0
right_count = 0

left_dir = 0
right_dir = 0

pTime = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.resize(img, (720, 690))

    timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

    img = detector.findPose(img, timestamp, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        right_angle = detector.findAngle(img, 12, 14, 16)
        right_per = np.interp(right_angle, (190, 260), (0, 100))

        # RIGHT COUNT
        if right_per == 100:
            if right_dir == 0:
                right_count += 0.5
                right_dir = 1

        if right_per == 0:
            if right_dir == 1:
                right_count += 0.5
                right_dir = 0

        left_angle = detector.findAngle(img, 11, 13, 15)
        left_per = np.interp(left_angle, (210, 330), (0, 100))

        # LEFT COUNT
        if left_per == 100:
            if left_dir == 0:
                left_count += 0.5
                left_dir = 1

        if left_per == 0:
            if left_dir == 1:
                left_count += 0.5
                left_dir = 0

        cv2.putText(img, f'Left: {int(left_count)}',
                    (50, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.putText(img, f'Right: {int(right_count)}',
                    (50, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(img, f'Total: {int(right_count)+int(left_count)}',
                    (50, 350), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (50, 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break