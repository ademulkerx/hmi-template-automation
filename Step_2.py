import pyautogui
import keyboard
import mouse
import time
import tkinter as tk
import winsound

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


    with open("Pos_List.txt", "r") as file:
        lines = file.readlines()


        # İlk satırdaki veriyi tag_position olarak al
        if lines:
            first_line = lines[0].strip()  # İlk satır
            x, y = map(int, first_line.split(":"))  # ':' ile ayır ve sayıya dönüştür
            tag_position = (x, y)
            print(f"Tag yazılacak pozisyon kaydedildi: {tag_position}")

    # Sonraki satırları ise led pozisyonu olarak kaydet
    for line in lines[1:]:
        line = line.strip()  # Satırdaki boşlukları temizle
        if line:
            x, y = map(int, line.split(":"))  # ':' ile ayır ve sayıya dönüştür
            led_positions.append((x, y))
            print(f"Nesne pozisyonu kaydedildi: ({x}, {y})")




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
            if i >= len(led_positions):
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

        if len(tags)-1 > len(led_positions):
            print("Uyarı: Fazla tag var. Daha fazla nesne pozisyonu gerekli.")
    except FileNotFoundError:
        print(f"TXT dosyası bulunamadı: {file_path}")

# Ana program
if __name__ == "__main__":
    print("Python program başladı.")
    time.sleep(3)

    winsound.Beep(1000, 100)
    time.sleep(0.3)
    winsound.Beep(1000, 100)
    time.sleep(0.3)
    winsound.Beep(1000, 100)


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



# Program  Otomatik algılanan ekrandaki nesnelerin taglarını yazar.
# step-1: Step_1.py ile tüm pozisyonlar alındıktan sonra bu program çalıştırılır ve ekranda herhangi bir konum değiştirilmemesi lazım.
# step-2: İşlem bitince 3 defa bip sesi gelir


# 13 Ocak 2025 | 13:21
# Yazar: Adem Ülker