import cv2
import mediapipe as mp
import pyautogui
import keyboard
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
run = True

def calculateEyeWay(x0, y0, x, y): #начало координат - точка левого верхнего угла глаза
    return [x - x0, y - y0]

def calculateRatio(screen_w, screen_h, eye_w, eye_h):
    return [screen_w / eye_w, screen_h / eye_h]
def calculate_center(leftX, rightX, topY, bottomY):
    x = abs(leftX + rightX) // 2
    y = abs(topY + bottomY) // 2
    return (x, y)

def printDotNumbers(x, y, id):
    cv2.putText(frame, str(id), (x - 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (246, 255, 12), 1)

while run:
    if keyboard.is_pressed("shift + s"): run = False
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    # для правого глаза:
    if landmark_points:
        landmarks = landmark_points[0].landmark
        coordinates = [[0, 0], [0, 0], [0, 0], [0, 0]]
        eyeLength = landmarks[388].x - landmarks[308].x
        eyeWidth = landmarks[387].y - landmarks[373].y
        center = [landmarks[473].x, landmarks[473].y]
        # print(int(landmarks[473].x * frame_w), int(landmarks[473].y * frame_h))
        cv2.circle(frame, (int(landmarks[473].x * frame_w), int(landmarks[473].y * frame_h)), 3, (0, 255, 0))
        screen_x = (screen_w * center[0] / (eyeWidth + 50))
        screen_y = (screen_h * center[1] / (eyeLength + 50))
        eyeWay = calculateEyeWay(landmarks[308].x, landmarks[387].y, landmarks[473].x, landmarks[473].y)
        print(eyeWay)
        ratio = calculateRatio(screen_w, screen_h, abs(eyeWidth), abs(eyeLength))
        # screen_x = screen_w * ratio[0]
        # screen_y = screen_h * ratio[1]
        # print(eyeWidth, eyeLength)
        # print(center)
        # print("----------")
        # pyautogui.moveTo(eyeWay[0] * ratio[0], eyeWay[1] * ratio[1])
        for id, landmark in enumerate(landmarks):
            print(landmark)
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            if id == 362:
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                # coordinates[id][0] = x
                # coordinates[id][1] = y
                # printDotNumbers(x, y, id)
        # x, y = calculate_center(coordinates[2][0], coordinates[0][0], coordinates[1][1], coordinates[3][1])
        # cv2.circle(frame, (x, y), 3, (0, 255, 0)) #рисуем центр
            # if id == 2:   # 0 - горизонтальное справа, 1 - вертикальная верхняя, 2 - горизонтальная правая, 3 - вертикальная нижняя
                # cv2.circle(frame, (x, y), 3, (0, 255, 0))
    #         if id == 1:
    #             screen_x = screen_w * landmark.x / frame_w
    #             screen_y = screen_h * landmark.y / frame_h
    #             pyautogui.moveTo(screen_x, screen_y)
    #     left = [landmarks[145], landmarks[159]]
    #     for landmark in left:
    #         x = int(landmark.x * frame_w)
    #         y = int(landmark.y * frame_h)
    #         cv2.circle(frame, (x, y), 3, (0, 255, 255))
    #     if (left[0].y - left[1].y) < 0.004:
    #         pyautogui.click()
    #         pyautogui.sleep(1)
        cv2.imshow('Eye Controlled Mouse', frame)
        # eye = frame[landmarks[373].y : landmarks[387].y, landmarks[308].x : landmarks[388].x]
        # cv2.imshow("Eye", eye)
        cv2.waitKey(1)

# для правого глаза -
# лево: 362, право: 388 # необходимо будет учесть, что зрачок не может до опорных точек доходить
# верх: 386, низ: 374
# 476 - левая точка самой радушки, 474 - правая точка радужки