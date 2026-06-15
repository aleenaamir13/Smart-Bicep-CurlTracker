import cv2
import numpy as np
import time
import PoseModule as pm

VIDEO_PATH = "curls.mp4"

RESIZE_WIDTH = 720
RESIZE_HEIGHT = 690

ALPHA = 0.9
ANGLE_MIN = 50
ANGLE_MAX = 160

L_PERCENT_UP = 75
L_PERCENT_DOWN = 25

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

detector = pm.poseDetector(MaxPoses=1, detectionCon=0.7, presenceCon=0.7, trackCon=0.7)

left_count = 0
left_dir = 0
left_counted = False

prev_l_angle = 0
pTime = 0

def smooth(prev, curr):
    return ALPHA * curr + (1 - ALPHA) * prev

while True:
    success, img = cap.read()
    if not success:
        break

    timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    img = cv2.resize(img, (RESIZE_WIDTH, RESIZE_HEIGHT))

    img = detector.findPose(img, timestamp, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:

        #left arm
        left_angle = detector.findAngle(img, 11, 13, 15, draw=True)
        left_angle = smooth(prev_l_angle, left_angle)
        prev_l_angle = left_angle

        left_per = np.interp(left_angle, (ANGLE_MIN, ANGLE_MAX), (100, 0))

        #state machine
        if left_per > L_PERCENT_UP and left_dir == 0:
            left_dir = 1
            left_counted = False

        if left_per < L_PERCENT_DOWN and left_dir == 1 and not left_counted:
            left_count += 1
            left_counted = True
            left_dir = 0

        # bar displaying
        bar_l = int(np.interp(left_per, (0, 100), (RESIZE_HEIGHT - 150, 100)))

        cv2.rectangle(img, (50, 100), (85, RESIZE_HEIGHT - 100), (255, 255, 255), 3)
        cv2.rectangle(img, (50, bar_l), (85, RESIZE_HEIGHT - 100), (0, 255, 0), cv2.FILLED)

        cv2.putText(img, f'{int(left_per)}%', (40, 80),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # left count display
    cv2.putText(img, f'Left : {left_count}', (50, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (RESIZE_WIDTH - 180, 650),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("Left Arm Curl Counter", img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"Left Reps : {left_count}")