import tkinter as tk
from PIL import ImageGrab, ImageTk, Image
import numpy as np
import cv2
import pyautogui
import time
import keyboard
import mouse
import winsound

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ekran Görüntüsü Seçici")

        # Pencereyi tam ekran yapma
        self.root.attributes('-fullscreen', True)  # Tam ekran
        self.root.attributes('-topmost', True)  # Üstte tut
        self.root.configure(bg='black')  # Arka plan siyah (yapılandırma için)

        # Ekran görüntüsünü al
        self.screenshot = ImageGrab.grab()
        self.screenshot_tk = ImageTk.PhotoImage(self.screenshot)

        # Ekran görüntüsünü göster
        self.canvas = tk.Canvas(root, width=self.screenshot.width, height=self.screenshot.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.screenshot_tk)
        self.canvas.pack()

        # Fare ile dikdörtgen seçim yapabilmek için
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        # Fare ile seçim başlatma ve bitirme
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Çıkış butonunu ekleyelim
        self.exit_button = tk.Button(self.root, text="Çıkış", command=self.quit_program,
                                     bg="red", fg="white", font=("Arial", 12), bd=0)
        self.exit_button.place(x=self.screenshot.width - 80, y=40)  # Sağ üst köşeye yerleştiriyoruz

        # Tag yazılacak pozisyonu seçmek için buton
        self.select_tag_position_button = tk.Button(self.root, text="Tag Yazılacak Konumu Seç ve Başlat",
                                                    command=self.select_tag_position, bg="green", fg="white",
                                                    font=("Arial", 12), bd=0)
        self.select_tag_position_button.place(x=self.screenshot.width - 300, y=10)  # Sağ üst köşeye

        # Tag pozisyonu ve tagları saklamak için
        self.tag_position = None
        self.led_positions = []  # LED pozisyonlarını saklayacak liste
        self.position_count = 0  # Pozisyon sayacı
        self.num_objects = 0  # Nesne sayısını burada başlatıyoruz
        self.tags = []  # Bu liste tagları tutacak


    def select_tag_position(self):
        """Tag yazılacak pozisyonunu seçmek için buton"""
        # Pencereyi gizleyelim, işlem arka planda devam etsin
        self.root.withdraw()  # Pencereyi gizleriz
        print("Tag yazılacak pozisyonu seçin...")

        # Başlangıçta tag pozisyonunu kaydetmek için bekliyoruz
        while True:
            if mouse.is_pressed(button='left'):  # Sol fare tuşu ile tıklama kontrolü
                x, y = mouse.get_position()
                winsound.Beep(1000, 100)
                self.tag_position = (x, y)
                print(f"Tag yazılacak pozisyon kaydedildi: {self.tag_position}")
                break  # Tag pozisyonu kaydedildikten sonra döngüden çıkıyoruz

            time.sleep(0.1)  # Kısa bir bekleme

        # Pozisyon toplamaya başla
        self.start_position_collection()

    def save_positions_to_file(self):
        """Pozisyonları dosyaya kaydetme"""
        with open("Pos_List.txt", "w") as file:
            # Tag yazılacak pozisyonu dosyaya ekliyoruz
            file.write(f"{self.tag_position[0]}:{self.tag_position[1]}\n")

            # LED pozisyonlarını yazıyoruz
            for led_pos in self.led_positions:
                file.write(f"{led_pos[0]}:{led_pos[1]}\n")

        """Pozisyonları dosyaya kaydetme shift yaparak kaydet labeller için"""
        with open("D:\PycharmProjects\Siemens\HMI\Sıralı_Label_Txt_Yazma_ai\Pos_List.txt", "w") as file:
            # LED pozisyonlarına + 35 ekleyerek label pozisyonlarını yazıyoruz
            for led_pos in self.led_positions:
                file.write(f"{led_pos[0]+35}:{led_pos[1]}\n")

        #

        print(f"Pozisyonlar 'Pos_List.txt' dosyasına kaydedildi.")
        winsound.Beep(1000, 100)
        time.sleep(0.3)
        winsound.Beep(1000, 100)
        time.sleep(0.3)
        winsound.Beep(1000, 100)
        self.root.quit()

    def start_position_collection(self):
        """LED pozisyonlarını toplamaya başlar"""
        print("Pozisyon toplamaya başla...")

        while True:
            if mouse.is_pressed(button='left'):  # Sol fare tuşu ile tıklama kontrolü
                x, y = mouse.get_position()

                if self.position_count == 0:
                    print(f"Tag pozisyonu kaydedildi: ({x}, {y})")
                else:
                    self.led_positions.append((x, y))
                    print(f"Nesne pozisyonu kaydedildi: ({x}, {y})")

                self.position_count += 1
                time.sleep(0.3)  # Tıklamalar arasında kısa bir bekleme

            if keyboard.is_pressed('enter'):  # Enter tuşu ile döngüyü sonlandırma
                print("Pozisyon toplama tamamlandı.")
                self.save_positions_to_file()
                break  # Döngüden çıkma



    def on_button_press(self, event):
        """Fare ile seçim başladığında (ilk tıklama)"""
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        """Fare ile seçim yapılırken (hareket ettikçe)"""
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        """Fare ile seçim bırakıldığında (ikinci tıklama)"""
        self.end_x = event.x
        self.end_y = event.y
        print(f"Seçilen alan: ({self.start_x}, {self.start_y}) - ({self.end_x}, {self.end_y})")

        # Seçilen alanı kırpma (crop)
        left = min(self.start_x, self.end_x)
        upper = min(self.start_y, self.end_y)
        right = max(self.start_x, self.end_x)
        lower = max(self.start_y, self.end_y)

        cropped_image = self.screenshot.crop((left, upper, right, lower))

        # Seçilen alanı numpy dizisine çevirme (OpenCV için)
        cropped_image_cv = np.array(cropped_image)
        cropped_image_cv = cv2.cvtColor(cropped_image_cv, cv2.COLOR_RGB2BGR)

        # Kırmızı nesneleri tespit et ve göster
        self.detect_red_objects(cropped_image_cv)

        # Ana resim üzerine gösterelim
        self.update_image()

    def detect_red_objects(self, image):
        """
        Bu fonksiyon, kırmızı renkli nesneleri tespit eder ve sıralar.
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

        red_mask = mask1 | mask2
        red_objects = cv2.bitwise_and(image, image, mask=red_mask)

        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_objects = []

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                detected_objects.append((x, y, w, h))

        detected_objects = sorted(detected_objects, key=lambda obj: obj[1])
        detected_objects = sorted(detected_objects, key=lambda obj: obj[0])

        self.detected_objects = []
        for (x, y, w, h) in detected_objects:
            real_x = x + self.start_x
            real_y = y + self.start_y
            self.detected_objects.append((real_x, real_y, w, h))

            # LED pozisyonlarını self.led_positions listesine ekle (Dairelerin merkez koordinatları)
            self.led_positions = [((x + w // 2) + self.start_x, (y + h // 2) + self.start_y) for (x, y, w, h) in detected_objects]

        self.num_objects = len(detected_objects)  # num_objects değerini güncelle

    def update_image(self):
        """
        Tkinter penceresinde, kırmızı nesnelerin numaralandırılmış olarak gösterilmesini sağlar.
        """
        img_with_objects = np.array(self.screenshot)
        img_with_objects = cv2.cvtColor(img_with_objects, cv2.COLOR_RGB2BGR)

        for idx, (x, y, w, h) in enumerate(self.detected_objects):
            cv2.rectangle(img_with_objects, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(img_with_objects, f"ID: {idx + 1}", (x+w+10, y +(int)(h/2)+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0),
                        2)

            # Dairenin merkezi
            center_x = x + w // 2
            center_y = y + h // 2

            # Merkezdeki minik daireyi çizme
            cv2.circle(img_with_objects, (center_x, center_y), 5, (0, 255, 0), -1)

        img_with_objects = cv2.cvtColor(img_with_objects, cv2.COLOR_BGR2RGB)
        img_with_objects_pil = ImageTk.PhotoImage(image=Image.fromarray(img_with_objects))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_with_objects_pil)
        self.screenshot_tk = img_with_objects_pil
        self.canvas.update()

        print(f"Tespit edilen {self.num_objects} nesne.")  # num_objects'ı buradan alıyoruz.

    def quit_program(self):
        """Programdan çıkmak için fonksiyon"""
        self.root.quit()



if __name__ == "__main__":
    time.sleep(3)
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()

    # Program  ekrandaki  (kırmızı) Led  nesnelerinin pozisyonlarını ve hemen yanındaki label konumlarınıda yakalar.
    # step-1: Ekran yakılnaştırma oranını %165(Hepsini algılayacak şekilde değiştirilebilir)
    # - şeklinde ayarla ve tag yazılacak ayar sayfasınıda tia portal dan kopar ve küçült bir kenarda dursun, tag yazılacak sekmede açık kalsın
    # step-2: program a start ver, 3 saniye sonra başlayacak ve hangi nesnelerde işlem olacak ise onları seç dikdörtgen ile(sol click nasılı tutarak)
    # step-3: Seçimden sonra doğrı sıra ile id yazıldı ise tag kaydetme butonuna(sağ üstte) tıkla ve tagların yazılacağı textboxa tıkla. 1 defa bip sesi gelirse kayıt tamamlanır
    #  1 defa bip sesi geldikten sonra programın kaydedilmesi için enter e bas.

    #  Pozsiyon kayıtlarını Pos_List.txt dosyasına yapacak ve ilk kayıt tag yazılacak textbox olacak, labellerin pozisyonu ise Sıralı_Label_Txt_Yazma_ai/Pos_List.txt yazacak.
    #  Label pozisyonlar ledlerden 35 pixel sağda olacak şekilde ayarlı sabit olarak ve gerekirse değiştirilebilir.

    #  Bu programdan sonra step 2 başlatılır ve program'a dokunulmaz.


    # 13 Ocak 2025 | 13:21
    # Yazar: Adem Ülker



