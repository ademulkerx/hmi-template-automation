import pyautogui
import keyboard
import mouse
import time
import tkinter as tk
import winsound

# Tıklanan pozisyonları saklayacak liste
label_positions = []

def show_icon(x, y, ClickValue):
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry('260x100+%d+%d' % (x + 10, y - 120))

    click_value = tk.StringVar()
    click_value.set(str(ClickValue))

    frame = tk.Frame(root, bg='black', padx=30, pady=10)  # Çerçeve genişliğini daha fazla artırdık
    frame.pack()

    # Tik işareti ve tıklama sayısı
    icon_label = tk.Label(frame, text="✅", fg='green', bg='black', font=("Helvetica", 60))
    icon_label.pack(side="left", padx=(0, 10))  # Sol kenara 10 piksel boşluk bırakıyoruz

    count_label = tk.Label(frame, textvariable=click_value, fg='green', bg='black', font=("Helvetica", 50),
                           justify='center', width=3)  # Genişlik özelliğini ekledik
    count_label.pack(side="left")

    root.attributes('-topmost', True)
    root.after(300, lambda: root.destroy())  # Pencereyi 300 ms sonra kapat
    root.mainloop()
sayac = 0
def collect_positions():
    global sayac
    """
    Kullanıcının tıklamalarını dinler ve koordinatları kaydeder.
    ESC tuşuna basıldığında kaydı durdurur.
    """
    print("Labellere tıklayın. ESC tuşuna bastığınızda kayıt tamamlanacak.")

    with open("Pos_List.txt", "r") as file:
        lines = file.readlines()


        # Sonraki satırları ise led pozisyonu olarak kaydet
    for line in lines:
        line = line.strip()  # Satırdaki boşlukları temizle
        if line:
            x, y = map(int, line.split(":"))  # ':' ile ayır ve sayıya dönüştür
            label_positions.append((x, y))
            print(f"Nesne pozisyonu kaydedildi: ({x}, {y})")





def paste_values_from_txt(file_path):
    """
    Kaydedilen pozisyonlara TXT dosyasındaki değerleri sırasıyla yapıştırır.
    :param file_path: TXT dosyasının yolu
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            values = file.readlines()  # Tüm satırları liste olarak oku
            values = [value.strip() for value in values]  # Satır sonu karakterlerini temizle

        print(f"{len(values)} değer yüklendi. İşleme başlanıyor...")

        for i, (x, y) in enumerate(label_positions):
            if i >= len(values):  # TXT'deki değerler tükendiğinde dur
                print("Tüm değerler yerleştirildi.")
                break

            # Labellere çift tıklama ve değer yapıştırma
            pyautogui.click(x, y, clicks=2, interval=0.1)  # Çift tıklama
            time.sleep(0.2)
            pyautogui.write(values[i])  # Değeri yaz
            print(f"Koordinat ({x}, {y}) konumuna '{values[i]}' yapıştırıldı.")
            time.sleep(0.2)
    except FileNotFoundError:
        print(f"TXT dosyası bulunamadı: {file_path}")


# Ana program
if __name__ == "__main__":
    print("Python program başladı.")
    time.sleep(3)
    # 1. Aşama: Pozisyonları toplama
    collect_positions()

    # 2. Aşama: TXT dosyasındaki verileri labellere yapıştırma
    txt_file_path = "data.txt"  # TXT dosyanızın yolu
    paste_values_from_txt(txt_file_path)
    winsound.Beep(1000, 100)
    time.sleep(0.3)
    winsound.Beep(1000, 100)
    time.sleep(0.3)
    winsound.Beep(1000, 100)
    print("İşlem tamamlandı.")



# Program  ekrandaki labellere otomatik bir şekilde veri yazar sırası ile.
# step-1: Sıralı_Adres(Name)_Led_Yazma_ai/Step_1.py ile pozisyonlar kaydedildikten sonra bu otomatik işlem kullanılır
# step-2: labellere yazılacak veri data.txt dosyasına kaydedilmiş olması gerekir.
# Programı başlattıktan sonra pycharmı hemen arka plana al ve dokunma pc ye, 3 saniye içinde yazma işlemi başlayacak.

# 8 Ocak 2025 | 04:51
# Yazar: Adem Ülker