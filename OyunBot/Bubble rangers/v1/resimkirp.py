import os
import cv2
import numpy as np

def select_roi(image_path):
    image = cv2.imread(image_path)
    print(image)
    clone = image.copy()
    roi_list = []
    cropping = False

    def crop_roi(event, x, y, flags, param):
        nonlocal cropping, roi_list

        if event == cv2.EVENT_LBUTTONDOWN:
            roi_list.append((x, y))
            cropping = True

        elif event == cv2.EVENT_LBUTTONUP:
            roi_list.append((x, y))
            cropping = False
            cv2.rectangle(image, roi_list[-2], roi_list[-1], (0, 255, 0), 2)
            cv2.imshow("Image", image)

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", crop_roi)

    while True:
        cv2.imshow("Image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):  # R tuşuna basarak seçimleri sıfırla
            image = clone.copy()
            roi_list = []

        elif key == 13:  # Enter tuşuna basarak seçilen alanları kırp ve kaydet
            for i in range(0, len(roi_list), 2):
                x1, y1 = roi_list[i]
                x2, y2 = roi_list[i + 1]
                cropped_roi = clone[y1:y2, x1:x2]
                cv2.imwrite(f"{os.path.splitext(image_path)[0]}_{i//2 + 1}.png", cropped_roi)

        elif key == ord("q"):  # Q tuşuna basarak resmi atlama
            break

    cv2.destroyAllWindows()

# Klasördeki her bir resme uygula
folder_path = r"C:/Users/furka/Desktop/isler/is2/dataset2/"
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
print(image_files)

for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)
    print(image_path)
    select_roi(image_path)
