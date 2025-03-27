import sys
import numpy as np
import cv2
import os

def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split(':')
            coords = parts[0].strip().split('-')
            x = float(parts[1].strip().replace(',', '.'))
            y1 = int(coords[0].strip())
            y2 = int(coords[1].strip())
            data.append((y1, y2, x))
    return data

def draw_static_elements(img):
    x_start, y_start = 15, 15
    width, height = 570, 220
    cv2.rectangle(img, (img.shape[1] - (x_start + width), img.shape[0] - y_start),
                  (img.shape[1] - x_start, img.shape[0] - (y_start + height)),
                  (255, 0, 0), 1)

    for n in range(17):
        for x_offset in [50, 60]:
            x, y = x_offset, ((n) * 15) + 5
            cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

def draw_data_on_image(data, product_number="Unknown"):
    img = np.full((250, 600, 3), 128, dtype=np.uint8)
    draw_static_elements(img)

    x_offset = 30
    for y1, y2, x in data:
        x_pos = img.shape[1] - (int(x) + x_offset)
        y1, y2 = img.shape[0] - y1, img.shape[0] - y2
        cv2.line(img, (x_pos, y1), (x_pos, y2), (0, 0, 255), 1)

    original_img = np.full((250, 600, 3), 128, dtype=np.uint8)
    for y1, y2, x in data:
        x_pos = original_img.shape[1] - (int(x) + x_offset)
        y1, y2 = original_img.shape[0] - y1, original_img.shape[0] - y2
        cv2.line(original_img, (x_pos, y1), (x_pos, y2), (0, 0, 255), 1)

    edges, error = preprocess_image(original_img)
    if error:
        print(error)

    largest_contour, error = find_contours(edges)
    if error:
        print(error)

    box = analyze_contour(largest_contour)
    width, height = calculate_rectangle_dimensions(box)

    en, boy = (height, width) if width > height else (width, height)

    img = cv2.putText(img, f'{product_number}', (340, 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)


    img = cv2.putText(img, f'En: {int(en)}', (90, 45), cv2.FONT_HERSHEY_PLAIN, 2, (255, 200, 200), 2, cv2.LINE_AA)
    img = cv2.putText(img, f'Boy: {int(boy)}', (70, 75), cv2.FONT_HERSHEY_PLAIN, 2, (200, 200, 255), 2, cv2.LINE_AA)
    cv2.drawContours(img, [box], 0, (0, 255, 255), 2)

    # Resmi debug/data/image dizinine kaydet
    output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "image")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_path = os.path.join(output_directory, f"{product_number}.png")
    cv2.imwrite(output_path, img)

    print("OK")
    print(int(en))
    print(int(boy))

def preprocess_image(image):
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return edges, None

def find_contours(edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, "Dikdörtgen bulunamadı."
    return max(contours, key=cv2.contourArea), None

def analyze_contour(contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    return np.intp(box)

def calculate_rectangle_dimensions(box):
    width = np.linalg.norm(box[0] - box[1])
    height = np.linalg.norm(box[1] - box[2])
    return width, height

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python ex_2.py <productNumber>")
        sys.exit(1)

    product_number = sys.argv[1]

    working_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(working_directory, 'BufferModel.txt')

    if not os.path.exists(file_path):
        print(f"Dosya {file_path} bulunamadı.")
        sys.exit(1)

    data = read_data_from_file(file_path)
    draw_data_on_image(data, product_number)
