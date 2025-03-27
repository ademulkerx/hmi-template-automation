import numpy as np
import cv2
from PIL import ImageGrab
from tensorflow.keras.models import load_model

# Eğitilmiş modeli yükle
model_path = 'D:\\PycharmProjects\\Image_Model_Egitme_V1\\model.h5'
model = load_model(model_path)

def predict_image(image):
    # Görüntüyü modelin beklediği forma dönüştür
    image = image.resize((28, 28))
    image = np.array(image)
    image = image / 255.0  # Normalizasyon
    image = np.expand_dims(image, axis=0)  # Model için doğru şekle getir

    # Tahmin yap
    prediction = model.predict(image)
    return prediction[0][0]

def screen_capture():
    # Ekranın belirli bir alanını izle
    screen_region = (0, 0, 800, 600)  # İzlenecek ekran alanı

    while True:
        # Ekranın bir bölgesini yakala
        screen = ImageGrab.grab(bbox=screen_region)
        screen = screen.convert('RGB')

        # Görüntü üzerinde tahmin yap
        prediction = predict_image(screen)

        # Tahmini yazdır
        if prediction > 0.5:  # Eğer "A" harfi olarak tespit edilirse
            print("A harfi tespit edildi!")

        # Bir sonraki frame için kısa bir mola ver
        cv2.waitKey(100)

if __name__ == '__main__':
    screen_capture()
