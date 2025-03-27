import cv2
import numpy as np
pol1 = [(83, 472), (0, 555), (0, 996), (213, 476)]
pol2 = [(213, 501), (74, 807), (476, 825), (315, 503)]
pol3 = [(213, 501), (74, 807), (476, 825), (315, 503)]
pol = pol3
listem = [pol1, pol2]
yol = r"C:\Users\furka\Desktop\isler\is2\resimler\tes.png"
cv2.namedWindow("resimç", cv2.WINDOW_NORMAL)
#trackbar oluştur

cv2.createTrackbar("x1", "resimç", pol[0][0], 1000, lambda x: x)
cv2.createTrackbar("y1", "resimç", pol[0][1], 1000, lambda x: x)
cv2.createTrackbar("x2", "resimç", pol[1][0], 1000, lambda x: x)
cv2.createTrackbar("y2", "resimç", pol[1][1], 1000, lambda x: x)
cv2.createTrackbar("x3", "resimç", pol[2][0], 1000, lambda x: x)
cv2.createTrackbar("y3", "resimç", pol[2][1], 1000, lambda x: x)
cv2.createTrackbar("x4", "resimç", pol[3][0], 1000, lambda x: x)
cv2.createTrackbar("y4", "resimç", pol[3][1], 1000, lambda x: x)
""" cv2.createTrackbar("x5", "resimç", pol[4][0], 1000, lambda x: x)
cv2.createTrackbar("y5", "resimç", pol[4][1], 1000, lambda x: x)
cv2.createTrackbar("x6", "resimç", pol[5][0], 1000, lambda x: x)
cv2.createTrackbar("y6", "resimç", pol[5][1], 1000, lambda x: x) """



resim = cv2.imread(yol)
while True:
    x1 = cv2.getTrackbarPos("x1", "resimç")
    y1 = cv2.getTrackbarPos("y1", "resimç")
    x2 = cv2.getTrackbarPos("x2", "resimç")
    y2 = cv2.getTrackbarPos("y2", "resimç")
    x3 = cv2.getTrackbarPos("x3", "resimç")
    y3 = cv2.getTrackbarPos("y3", "resimç")
    x4 = cv2.getTrackbarPos("x4", "resimç")
    y4 = cv2.getTrackbarPos("y4", "resimç")
    #x5 = cv2.getTrackbarPos("x5", "resimç")
    #y5 = cv2.getTrackbarPos("y5", "resimç")
    #x6 = cv2.getTrackbarPos("x6", "resimç")
    #y6 = cv2.getTrackbarPos("y6", "resimç")
    pol = [(x1, y1),(x2,y2), (x3, y3), (x4, y4)]
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    resim = cv2.imread(yol)
    for i in listem:
        cv2.polylines(resim, [np.array(i, np.int32)], True, (255, 0, 255), 2)
    cv2.polylines(resim, [np.array(pol, np.int32)], True, (255, 0, 255), 2)
    cv2.imshow("resim", resim[:,:])
    key = cv2.waitKey(1)
    if key == 27:
        break
print(pol)
