import cv2
import numpy as np
import os
import random
from math import cos, sin, radians
import uuid


def create_rotated_rectangle(image, center, size, angle, color):
    w, h = size
    rect = np.array([
        [-w / 2, -h / 2],
        [w / 2, -h / 2],
        [w / 2, h / 2],
        [-w / 2, h / 2]
    ])

    theta = radians(angle)
    rotation_matrix = np.array([
        [cos(theta), -sin(theta)],
        [sin(theta), cos(theta)]
    ])

    rotated_rect = np.dot(rect, rotation_matrix) + center
    rotated_rect = np.int0(rotated_rect)

    cv2.drawContours(image, [rotated_rect], 0, color, -1)


def create_synthetic_images(output_dir, num_images, image_size=(1000, 500), rect_size_range=(20, 300),
                            angle_range=(0, 180)):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_images):
        image = np.ones((image_size[1], image_size[0], 3), dtype=np.uint8) * 255  # Beyaz arka plan

        center_x = random.randint(0, image_size[0])
        center_y = random.randint(0, image_size[1])
        width = random.randint(rect_size_range[0], rect_size_range[1])
        height = random.randint(rect_size_range[0], rect_size_range[1])
        angle = random.randint(angle_range[0], angle_range[1])
        color = (0, 0, 0)  # Siyah dikdörtgen

        create_rotated_rectangle(image, (center_x, center_y), (width, height), angle, color)

        unique_id = uuid.uuid4().hex  # Benzersiz bir tanımlayıcı oluştur
        filename = f"image_{unique_id}_w{width}_h{height}_a{angle}.png"
        cv2.imwrite(os.path.join(output_dir, filename), image)


# Kullanıcıdan kaç adet görüntü üretileceğini alın
num_images = int(input("Kaç adet görüntü üretmek istiyorsunuz? "))
output_dir = 'synthetic_images'  # Görüntülerin kaydedileceği dizin

# Sentetik veri setini oluştur
create_synthetic_images(output_dir, num_images)

print(f"{num_images} adet görüntü {output_dir} dizinine kaydedildi.")
