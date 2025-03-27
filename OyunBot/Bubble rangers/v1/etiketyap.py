import cv2
import numpy as np
import pandas as pd
from PIL import ImageGrab
import pyautogui
from ultralytics import YOLO
import torch
import time

islem2 = True
model = YOLO('best_openvino_model')

def is_object_in_area(x1, y1, x2, y2, area):
    result = cv2.pointPolygonTest(np.array(area, np.int32), (int(x1+((x2-x1)/2)), int(y1+(y2-y1))), False)
    return result >= 0

while True:
    
    window = pyautogui.getWindowsWithTitle("ldplayer")
    a = time.time()
    # Uygulamanın penceresini bul
    if window and window[0].isActive:
        window = window[0]
        # Uygulamanın ekran görüntüsünü al
        left, top, width, height = window.left, window.top, window.width, window.height
        # Aranan görüntüyü yükle
    
        screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        screenshot = cv2.normalize(screenshot, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
        results = model(screenshot)
        txt_icerigi = []
        for r in results:
            boxes = r.boxes
            boxe = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xywhn[0]
                x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
                class_id = box.cls
                class_id = int(class_id)
                if type(class_id) == int:
                    liste = [class_id,x1,y1,x2,y2]
                    txt_icerigi.append(liste)
        if len(txt_icerigi) >0:
            with open(f"deneme/{a}.txt", "w") as f:
                for i in txt_icerigi:
                    i = str(i).replace("[","").replace("]","").replace(",","")
                    f.write(str(i))
                    f.write("\n")
                print(txt_icerigi)
            cv2.imwrite(f"deneme/{a}.png", screenshot)
    else:
        time.sleep(0.75)
        print("ldplayer uygulaması bulunamadı.")