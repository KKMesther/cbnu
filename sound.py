import cv2
import numpy as np
import pygame
import pyautogui

# 이미지 경로
target_image_path = "D:\\label.jpg"

# 매칭 임계값
threshold = 0.6

# 사운드 경로
siren_sound_path = "D:\\sairen.mp3"

# 초기화
pygame.init()
pygame.mixer.init()
siren_sound = pygame.mixer.Sound(siren_sound_path)

# 이미지 로드
target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
target_height, target_width = target_image.shape[::-1]

while True:
    # 캡쳐
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 캡쳐 매칭
    result = cv2.matchTemplate(screenshot, target_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 매칭결과 확인
    if max_val > threshold:
        if siren_sound.get_num_channels() == 0:
            siren_sound.play()
            print("Target image detected! Siren activated.")
    else:
        if siren_sound.get_num_channels() > 0:
            siren_sound.stop()
            print("Target image not detected. Siren stopped.")
    
    
    cv2.waitKey(1000)
