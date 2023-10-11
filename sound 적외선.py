import cv2
import numpy as np
import pygame

def fire_detection(frame):
    # 이미지를 색 공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨간 범위 설정
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # 노란 범위 설정
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 빨간색과 노란색 합침
    mask_combined = cv2.bitwise_or(mask_red, mask_yellow)


    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_combined)

    #  화재영역 바운딕 박스
    for i in range(1, num_labels):
        x, y, w, h, area = stats[i]
        if area > 100:  # 화재로 판단할 영역
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame

if __name__ == "__main__":
    # 웹캠 스트리밍
    cap = cv2.VideoCapture(0)  # 웹캠 사용 시 0, IP 카메라는 URL 입력


    pygame.init()


    fire_sound = pygame.mixer.Sound("D:/sairen.mp3")  # 사이렌 경로

    playing_sound = False  # 사운드 재생 여부
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result_frame = fire_detection(frame)

        # 검출된 화재영역 보이면 사운드 재생
        if np.any(result_frame[:, :, 1] == 255):  # 바운딩 박스 검출된 화재 여부 확인
            if not playing_sound:
                fire_sound.play()
                playing_sound = True
        else:
            if playing_sound:
                fire_sound.stop()
                playing_sound = False

        cv2.imshow("Fire Detection Result", result_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()  # pygame 리소스 
