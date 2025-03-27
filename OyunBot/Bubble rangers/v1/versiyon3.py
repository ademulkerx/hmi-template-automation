import pyautogui
import time
from PIL import ImageGrab, Image
import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd
import keyboard
import dxcam
camera = dxcam.create()
pol1 = [(124, 434), (0, 551), (0, 996), (220, 456), (211, 425), (178, 413)]
pol2 = [(220, 461), (101, 737), (438, 751), (288, 422), (247, 413), (225, 418)]
pol3 = [(306, 456), (537, 1000), (548, 562), (355, 400), (312, 434), (303, 447)]
pol4 = [(83, 472), (0, 555), (0, 996), (213, 476)]
pol5 = [(218, 454), (103, 742), (436, 762), (308, 456)]
pol6 = [(319, 481), (537, 1000), (575, 557), (431, 476)]
ana = [(200, 503), (74, 807), (476, 825), (333, 517), (294, 479), (263, 499), (234, 479)]
duvaricin = [(213, 521), (74, 807), (476, 825), (317, 521)]
listem = [pol1,pol2, pol3,pol4,pol5,pol6]
play = Image.open("resimler/play.png")
start = Image.open("resimler/start.png")
skip = Image.open("resimler/skip.png")
#watch = Image.open("resimler/watchad.png")
xpng = Image.open("resimler/x.png")
close1 = Image.open("resimler/close.png")
close2 = Image.open("resimler/closee.png")
reklamkapa = Image.open("resimler/reklamkapat.png")
skip1 = Image.open("resimler/skip.png")
skip2 = Image.open("resimler/skip2.png")
skip3 = Image.open("resimler/skip3.png")
skip4 = Image.open("resimler/skipvideo.png")
skip5 = Image.open("resimler/kot.png")
islem = True
islem2 = True
cameraac = True
model = YOLO('best_openvino_model')
neredeyim = 2
def is_object_in_area(x1, y1, x2, y2, area):
    result = cv2.pointPolygonTest(np.array(area, np.int32), (int(x1+((x2-x1)/2)), int(y1+(y2-y1))), False)
    return result >= 0
a1 = time.time()
a2 = a1
a3 = a1
a4 = a1
a5 = a1
a6 = a1
a7 = a1
a8 = a1
a9 = a1
a10 = a1

sasa = True
while True:
    sag_dolu = False
    sol_dolu = False
    window = pyautogui.getWindowsWithTitle("ldplayer")
    # Uygulamanın penceresini bul
    if window or window[0].isActive:
        window = window[0]
        left, top, width, height = window.left, window.top, window.width, window.height
        if cameraac:
            camera.start(target_fps=60,region=(left, top, left + width, top + height))  # threaded
            cameraac = False
        # Uygulamanın ekran görüntüsünü al
        # Aranan görüntüyü yükle
        if islem:
            screenshot = camera.get_latest_frame()  # Will block until new frame available
            screenshot = ImageGrab.grab(bbox=(left, top + height/2, left + width, top + height))
            search_image = start
            try:
                result = pyautogui.locate(search_image, screenshot, confidence=0.8)
                x, y = result.left + left + result.width // 2, result.top + top +height//2 +  result.height // 2
                print(f"Görüntü ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                pyautogui.click(x, y,duration=0.1)  # Görüntüyü tıkla
                x, y = left + int((width // 2)), top + (height // 2)
                pyautogui.moveTo(x,y,duration=0)
                islem = False
                search_image = skip
                sorgu = time.time()
                sorgu2 = time.time()
            except:
                pass
            
        else:
            screenshot = camera.get_latest_frame()
            af = screenshot.copy()
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
            results = model.predict(screenshot, conf=0.5)
            bounding_boxes = results[0].boxes.data
            if len(bounding_boxes) == 0:
                 sorgu2 = time.time()
                 time.sleep(0.2)
            else:
                sorgu = time.time()
            px = pd.DataFrame(bounding_boxes).astype("float")
            yap = True
            for index, row in px.iterrows():
                x1, y1, x2, y2, d = map(int, row[[0, 1, 2, 3, 5]])
                d = int(d)
                if d == 0 or d == 1 or d == 2 or d == 3 or d == 4 or d == 5 or d == 6 or d == 7 or d == 8:
                    if is_object_in_area(x1, y1, x2, y2, pol1):
                        sol_dolu = True
                    if is_object_in_area(x1, y1, x2, y2, pol3):
                        sag_dolu = True
            if sasa:
                pyautogui.mouseDown(button='left')
                pyautogui.moveTo(x, y-30,duration=0.1)
                pyautogui.mouseUp(button='left')
                pyautogui.moveTo(x,y,duration=0)
                sasa = False
                
            for index, row in px.iterrows():
                x1, y1, x2, y2, d = map(int, row[[0, 1, 2, 3, 5]])
                d = int(d)
                
                if d == 9 or d == 10:
                    if is_object_in_area(x1, y1, x2, y2, ana):
                        yap = False
                if d == 0 or d == 1 or d == 8:
                    if is_object_in_area(x1, y1, x2, y2, ana):
                        pyautogui.mouseDown(button='left')
                        pyautogui.moveTo(x, y-30,duration=0.1)
                        pyautogui.mouseUp(button='left')
                        pyautogui.moveTo(x,y,duration=0)
                        print("Sol üstteki nesneyi tıkladı")
                    #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                elif d == 2 or d == 4:
                    if is_object_in_area(x1, y1, x2, y2, ana):
                        pyautogui.mouseDown(button='left')
                        pyautogui.moveTo(x, y+30,duration=0.1)
                        pyautogui.mouseUp(button='left')
                        pyautogui.moveTo(x,y,duration=0)
                    
                    #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                elif is_object_in_area(x1, y1, x2, y2, pol5):
                    if d == 5 or d == 6 or d == 7:
                        if d == 6:
                            if is_object_in_area(x1, y1, x2, y2, duvaricin):
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x, y-30,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x, y-60,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                        if d == 5 or d == 7:
                            pyautogui.mouseDown(button='left')
                            pyautogui.moveTo(x, y-30,duration=0.1)
                            pyautogui.mouseUp(button='left')
                            pyautogui.mouseDown(button='left')
                            pyautogui.moveTo(x, y-60,duration=0.1)
                            pyautogui.mouseUp(button='left')
                            pyautogui.moveTo(x,y,duration=0)
                        #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    elif neredeyim == 2:
                        if d == 3:
                            if not sol_dolu:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x-30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 1
                                print("Ortadayken oyunkolu tespit etti sola geçti")
                            else:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x+30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 3
                                print("Ortadayken oyunkolu tespit etti sağa geçti")
                    elif neredeyim == 1:
                        if d == 3:
                            if True:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x+30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 2
                                print("Soldayken oyun kolu tespit edildi ortaya geçti")

                                
                    elif neredeyim == 3:
                        if d == 3:
                            if True:
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x-30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 2
                                print("Sağdayken oyun kolu tespit edildi ortaya geçti")
            if yap and not sag_dolu and not sol_dolu:
                for index, row in px.iterrows():
                    x1, y1, x2, y2, d = map(int, row[[0, 1, 2, 3, 5]])
                    d = int(d)
                    if d == 10 and time.time() - a4 > 30:
                        farkk = 10
                        a4 = time.time()
                    else:
                        farkk = 0.5
                    if d == 9 or d == 10:
                        if neredeyim == 2 and time.time() - a7 > farkk:
                            if is_object_in_area(x1, y1, x2, y2, pol6):
                                #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x+30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 3
                                a7 = time.time()
                                print("Ortadayken para bulduğu için sağa geçti")
                            elif is_object_in_area(x1, y1, x2, y2, pol4) and time.time() - a7 > 0.5:
                                #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x-30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 1
                                print("Ortadayken para bulduğu için sola geçti")
                                a7 = time.time()
                        elif neredeyim == 1 and time.time() - a7 > farkk:
                            if is_object_in_area(x1,y1,x2,y2,pol6):
                                #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x+30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 2
                                print("Soldayken para bulduğu için Ortadaya geçti")
                                a7 = time.time()
                        elif neredeyim == 3 and time.time() - a7 > farkk:
                            if is_object_in_area(x1,y1,x2,y2,pol4):
                                #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                pyautogui.mouseDown(button='left')
                                pyautogui.moveTo(x-30, y,duration=0.1)
                                pyautogui.mouseUp(button='left')
                                pyautogui.moveTo(x,y,duration=0)
                                neredeyim = 2             
                                print("Sağdayken para bulduğu için Ortadaya geçti")
                                a7 = time.time()          
                    #cv2.rectangle(screenshot, (x1, y1), (x2, y2), (0, 255, 0), 2)
                print(neredeyim)
            hiztest =  time.time()
            if sorgu2-sorgu > 2:
                try:
                    search_image = play
                    result = pyautogui.locate(search_image, af, confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0.1)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try1")
                    neredeyim = 2
                    time.sleep(1)
                    sasa = True
                    listem = [pol1,pol2, pol3,pol4,pol5, pol6]
                except:
                    pass
                try:
                    search_image = skip
                    result = pyautogui.locate(search_image, af, confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try2")
                    time.sleep(1)

                except:
                    pass
                try:
                    search_image = xpng
                    result = pyautogui.locate(search_image, af[60:140,:], confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)+60
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try3")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = close1
                    result = pyautogui.locate(search_image, af, confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)+60
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try4")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = close2
                    result = pyautogui.locate(search_image, af[60:140,:], confidence=0.8)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)+60
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try5")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = reklamkapa
                    result = pyautogui.locate(search_image, af, confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)+60
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try6")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = skip1
                    result = pyautogui.locate(search_image, af, confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try7")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = skip2
                    result = pyautogui.locate(search_image, af, confidence=0.9)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try8")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = skip3
                    result = pyautogui.locate(search_image, af, confidence=0.9)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try9")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = skip4
                    result = pyautogui.locate(search_image, af, confidence=0.7)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try10")
                    time.sleep(1)
                except:
                    pass
                try:
                    search_image = skip5
                    result = pyautogui.locate(search_image, af, confidence=0.9)
                    xs, ys = result.left + left+ (result.width//2), result.top + top + (result.height//2)
                    print(f"Görüntü play ldplayer penceresinde bulundu. Konum: ({x}, {y})")
                    pyautogui.click(xs, ys,duration=0)  # Görüntüyü tıkla
                    pyautogui.moveTo(x,y,duration=1)
                    print("try10")
                    time.sleep(1)
                except:
                    pass
                hiztest2 = time.time()
                print(hiztest2-hiztest)
            for i in listem:
                cv2.polylines(screenshot, [np.array(i, np.int32)], True, (255, 0, 255), 2)
            cv2.polylines(screenshot, [np.array(ana, np.int32)], True, (255, 0, 0), 2)
            cv2.imshow("Ekran Görüntüsü", screenshot)
            key = cv2.waitKey(30)
            if key == 27:
                break
            if keyboard.is_pressed("q"):
                break
            if time.time() - a10 >= 60:
                print("******************************************************************")
                listem = [pol1,pol2, pol3,pol1,pol2, pol3]
                a10 = time.time()
    else:
        time.sleep(1)
        print("ldplayer uygulaması bulunamadı.")
cv2.destroyAllWindows()
camera.stop()

# Örnek bir resim yolu ve uygulama başlığı