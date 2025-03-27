# Bu program kusursuz bir dikdörtgeni çok iyi bir şekilde ölçebiliyor.
# yani bundan önceki adımda kusursuz bir dikdörtgen yapılacak


import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_image(title, image):
    plt.figure(figsize=(10, 10))
    plt.title(title)
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

def preprocess_image(image_path):
    # Resmi yükle
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None, "Resim yüklenemedi."

    # Gri tonlamaya çevirme (zaten gri tonlamada yüklüyoruz)
    # Bulanıklaştırma
    blurred = cv2.GaussianBlur(image, (5, 5), 0)

    # Kenar algılama
    edges = cv2.Canny(blurred, 50, 150)

    # Görüntüleri göster
    # display_image("Orijinal Görüntü", image)
    # display_image("Bulanıklaştırılmış Görüntü", blurred)
    # display_image("Kenar Algılama", edges)

    return edges, None

def find_contours(edges):
    # Konturları bul
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None, "Dikdörtgen bulunamadı."

    # En büyük konturu seç (dikdörtgeni temsil eden)
    largest_contour = max(contours, key=cv2.contourArea)

    return largest_contour, None

def analyze_contour(contour):
    # Kontur için minimum alan kaplayan dikdörtgeni bul
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    return box

def calculate_rectangle_dimensions(box):
    # Dikdörtgenin köşe noktaları arasındaki mesafeleri hesapla
    width = np.linalg.norm(box[0] - box[1])
    height = np.linalg.norm(box[1] - box[2])

    return width, height

# Dosya yolunu buraya ekleyin
image_path = 'img/1.png'
edges, error = preprocess_image(image_path)
if error:
    print(error)

largest_contour, error = find_contours(edges)
if error:
    print(error)

box = analyze_contour(largest_contour)
width, height = calculate_rectangle_dimensions(box)

if width > height:
    en = height
    boy = width
else:
    boy = height
    en = width
print(f"En: {en}")
print(f"Boy: {boy}")

# Dikdörtgeni çiz ve göster
image_with_rectangle = cv2.imread(image_path)
cv2.drawContours(image_with_rectangle, [box], 0, (0, 0, 255), 2)
display_image("Dikdörtgen", image_with_rectangle)
