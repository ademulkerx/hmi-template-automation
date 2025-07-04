import pyautogui
import keyboard
import mouse
import time
import tkinter as tk
import winsound

# TkLiteUI modülü:
import TkLiteUI as tl


# Pozisyonları saklayacak değişkenler
tag_position = None
led_positions = []

def show_icon(x, y, ClickValue):
    """Tıklanan pozisyonu görselleştirir."""
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry('260x100+%d+%d' % (x + 10, y - 120))

    click_value = tk.StringVar()
    click_value.set(str(ClickValue))

    frame = tk.Frame(root, bg='black', padx=30, pady=10)
    frame.pack()

    icon_label = tk.Label(frame, text="✅", fg='green', bg='black', font=("Helvetica", 60))
    icon_label.pack(side="left", padx=(0, 10))

    count_label = tk.Label(frame, textvariable=click_value, fg='green', bg='black', font=("Helvetica", 50),
                           justify='center', width=3)
    count_label.pack(side="left")

    root.attributes('-topmost', True)
    root.after(300, lambda: root.destroy())  # Pencereyi 300 ms sonra kapat
    root.mainloop()

def collect_positions():
    """
    Kullanıcının tıklamalarını dinler:
    - İlk tıklama tag yazılacak alanı belirler.
    - Sonraki tıklamalar nesne pozisyonlarını kaydeder.
    ESC tuşuna basıldığında pozisyon toplama tamamlanır.
    """
    global tag_position, led_positions
    position_count = 0

    print("İlk tıklama tag yazılacak pozisyonu belirleyecek. Sonraki tıklamalar LED pozisyonlarını belirleyecek.")
    print("ESC tuşuna bastığınızda kayıt tamamlanacak.")

    while True:
        if mouse.is_pressed(button='left'):


            x, y = mouse.get_position()

            if position_count == 0:
                tag_position = (x, y)
                print(f"Tag yazılacak pozisyon kaydedildi: ({x}, {y})")
                show_icon(x, y, "0")
            else:
                led_positions.append((x, y))
                print(f"Nesne pozisyonu kaydedildi: ({x}, {y})")
                show_icon(x, y, position_count)
            position_count += 1
            time.sleep(0.3)

        if keyboard.is_pressed('enter'):  # ESC tuşuna basıldığında döngüyü kır
            print("Pozisyon toplama tamamlandı.")
            break

def write_tags_from_txt(file_path):
    """
    Kaydedilen pozisyonlara TXT dosyasındaki tagları sırasıyla yazar.
    :param file_path: TXT dosyasının yolu
    """
    global tag_position, led_positions

    if tag_position is None or not led_positions:
        print("Pozisyonlar eksik. Tag pozisyonu veya nesne pozisyonları kaydedilmemiş.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tags = file.readlines()
            tags = [tag.strip() for tag in tags]

        print(f"{len(tags)} tag yüklendi. İşleme başlanıyor...")

        for i, (x, y) in enumerate(led_positions):
            if i >= len(tags):
                print("Tüm taglar yerleştirildi. Fazla nesneler atlandı.")
                break

            # LED'e tıklama
            pyautogui.click(x, y)
            time.sleep(0.2)

            # Tag yazma alanına çift tıklama
            pyautogui.click(tag_position[0], tag_position[1], clicks=2, interval=0.1)
            time.sleep(0.3)

            # Tagı yazma Eğer Boş ise Biir defa back space yap
            if tags[i] == "":
                keyboard.press_and_release('backspace')
            else:
                keyboard.write(tags[i])

            print(f"Nesne ({x}, {y}) için '{tags[i]}' tagı yazıldı.")
            time.sleep(0.3)
            # Enter'e tıkla
            keyboard.press_and_release('enter')
            time.sleep(0.4)

        if len(tags) > len(led_positions):
            print("Uyarı: Fazla tag var. Daha fazla nesne pozisyonu gerekli.")
    except FileNotFoundError:
        print(f"TXT dosyası bulunamadı: {file_path}")

# -- Ana işlemleri tek bir fonksiyona topluyoruz (main). --
def main():
    print("Python program başladı.")

    # 1. Aşama: Pozisyonları toplama
    collect_positions()

    # 2. Aşama: TXT dosyasından tagları okuma ve yazma
    txt_file_path = "data.txt"  # TXT dosyasının yolu
    write_tags_from_txt(txt_file_path)

    # Bitirme sesi
    winsound.Beep(1000, 100)
    time.sleep(0.3)
    winsound.Beep(1000, 100)
    time.sleep(0.3)
    winsound.Beep(1000, 100)

    print("İşlem tamamlandı.")



# -- TkLiteUI Arayüz Kodları --
#  1) UI sınıfından bir örnek oluşturuyoruz
ui = tl.ui()

#  2) Bir pencere oluşturuyoruz
pencere = ui.create_window(title="LED Tag Yazma Programı", width=500, height=200, bg="lightgray")

#  3) "Başlat" butonunu ekliyoruz
baslat_butonu = ui.add_button(
    pencere=pencere,
    text="Başlat",
    button_x=10,
    button_y=10,
    button_width=120,
    button_height=40,
    on_click={'action': main}  # Tıklanınca main fonksiyonunu çalıştır
)

# 4) Uygulama döngüsünü başlat
ui.StartMainWindow(pencere)
