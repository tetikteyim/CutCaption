# CutCaption - Video Kesme Otomasyonu

# Bu kod, tanımlı klasördeki tüm videoları tarar,
# Altyazılar içinde belirli bir kelimeyi bulur ve kelimenin geçtiği kısımları keserek kaydeder.

#       Version 2 ---------------------------------------------
# srt dosyasından seçilen kelimelerin, videodaki zamanlarını bulma
# Bulunan zamanları videoda kesme

#       Version 3 ---------------------------------------------
# Kesilen videoları belirlenen bir OUTPUT klasörüne kaydetme eklendi

#       Version 4 ---------------------------------------------
# Dosya isimlerine timecode eklendi

#       Version 5 ---------------------------------------------
# dosya ismindeki <>:"/\\|?* ve <boşluk> karakterleri "_" ile değiştirme eklendi

#       Version 6 ---------------------------------------------
# dosya ismindeki türkçe karakterleri ingilizce karşılığına çeviren bie eklenti yapıldı

#       Version 6.1 ---------------------------------------------
# Daha iyi dosya adlandırma: Dosya ismindeki tüm harfler küçük harflere dönüştürüldü.
# Altyazı dosyası açılırken oluşabilecek hatalar yakalanıyor
# Gereksiz tekrarlar azaltıldı: sanitize_filename ve replace_turkish_chars fonksiyonları düzenlendi.
# FFmpeg komutunu iyileştirildi: Gereksiz parametreler çıkarıldı, daha stabil çalışması sağlandı

#       Version 6.2 ---------------------------------------------
# Geliştirilmiş FFmpeg Komutları ve Dosya İsmi Düzenleme
# sanitize_filename fonksiyonunda .mp4 uzantısının kesin eklenmesi
# FFmpeg komutunda hata yakalama mekanizması eklenmesi
# Dosya işleme sırasında detaylı log eklenmesi

#       Version 7 ---------------------------------------------
# Arayüz eklendi! Artık videoların ve altyazıların olduğu klasörü, çıkış klasörünü ve aranacak kelimeyi bir pencere üzerinden seçerek işlemi başlatabilirsiniz. 

#       Version 7.1 ---------------------------------------------
# Arayüzde o anda hangi dosyanın işlendiğini ve işlemler bittiğinde kaç tane video kestiğini belirten bir eklenti yapıldı

#       Version 7.2 ---------------------------------------------
# Arayüzdeki bilgilerin refresh hatalarıdüzeltildi

#       Version 7.3 ---------------------------------------------
# kesilen videoların başına ve sonuna 1 saniye eklendi

#       Version 7.4 ---------------------------------------------
# Arayüze bitrate ayarını da eklendi

#       Version 7.5 ---------------------------------------------
# Arayüze bitrate ayarını kbps olarak girme eklendi

#       Version 7.6 ---------------------------------------------
# İyileştirmeler yapıldı

#       Version 7.7 ---------------------------------------------
# process_videos_in_folder fonksiyonuna toplam video sayısını ve kesilecek video sayısını belirten kod eklendi.
# Kullanıcıya işlem sırasındaki gelişmeleri göstermek için arayüzdeki etiketler güncellendi.
# İşlem tamamlandığında kullanıcıya bilgi mesajı gösterilmesi sağlandı
# Start düğmesi başlangıçta yeşil renkte olacak, işlemler başladığında kırmızı renge dönecek ve işlemler tamamlandığında tekrar yeşil renge dönme özelliği eklendi

#       Version 8 ---------------------------------------------
# Arayüz düzenlemeleri yapıldı

#       Version 8.1 ---------------------------------------------
# Dosya ismine bitrate eklendi
# Kesilme işlemi yapılan video dosyasına eklenen timecode'u kısaltmak için start ve end zamanlarının sadece saat, dakika ve saniye kısmını kullanıldı
# dosya ismine eklenen bitrate değeri 1000 ile bölünerek yazıldı ve 'mbps' olarak belirtildi

#       Version 8.2 ---------------------------------------------
# Terminal çıktıları anlık olarak arayüzde gösterilecek ve işlemler tamamlandığında çıkan mesaj ana arayüzde görünecek.
# İşlem bitti uyarı penceresi kalktı

import os
import pysrt
import re
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, timedelta

# Global variables to control the stop process
stop_processing = False

def replace_turkish_chars(text):
    """Türkçe karakterleri İngilizce eşdeğerlerine çevirir ve küçük harfe dönüştürür."""
    turkish_map = {
        "ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
        "Ç": "c", "Ğ": "g", "İ": "i", "Ö": "o", "Ş": "s", "Ü": "u"
    }
    return re.sub(r'[^a-zA-Z0-9_]', '_', ''.join(turkish_map.get(c, c) for c in text)).lower()

def sanitize_filename(filename):
    """Dosya adındaki yasaklı karakterleri temizler ve uzantıyı ekler."""
    sanitized = replace_turkish_chars(filename).strip("_")
    if not sanitized.endswith(".mp4"):
        sanitized += ".mp4"
    return sanitized

def find_word_in_srt(srt_file, keyword):
    """Altyazı dosyasında belirli bir kelimeyi bulup başlangıç ve bitiş zamanlarını döndürür."""
    try:
        subs = pysrt.open(srt_file, encoding='utf-8')
    except Exception as e:
        log_message(f"⚠️ Hata: {srt_file} dosyası açılamadı. {e}")
        return []
    
    matches = []
    for sub in subs:
        if re.search(rf"\b{keyword}\b", sub.text, re.IGNORECASE):
            matches.append((str(sub.start.to_time()), str(sub.end.to_time())))
    
    return matches

def adjust_time(time_str, delta_seconds):
    """Verilen zaman stringine belirtilen saniye ekler veya çıkarır."""
    if '.' not in time_str:
        time_str += '.000'
    time_obj = datetime.strptime(time_str, "%H:%M:%S.%f")
    adjusted_time = time_obj + timedelta(seconds=delta_seconds)
    return adjusted_time.strftime("%H:%M:%S.%f")[:-3]

def cut_video(video_file, start_time, end_time, output_file, bitrate_kbps):
    """FFmpeg kullanarak videoyu belirli zaman aralığında keser ve hataları yakalar."""
    start_time_adjusted = adjust_time(start_time, -1)
    end_time_adjusted = adjust_time(end_time, 1)
    
    bitrate = f"{bitrate_kbps}k"
    
    command = [
        "ffmpeg", "-i", video_file, "-ss", start_time_adjusted, "-to", end_time_adjusted,
        "-c:v", "libx264", "-b:v", bitrate, "-c:a", "aac", "-b:a", "128k", "-y", output_file
    ]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            log_message(f"✅ Kesme işlemi başarılı: {output_file}")
        else:
            log_message(f"⚠️ FFmpeg Hatası: {result.stderr}")
            log_message(f"Komut: {' '.join(command)}")
    except Exception as e:
        log_message(f"⚠️ FFmpeg çalıştırılamadı: {e}")

def process_videos_in_folder(folder_path, keyword, output_folder, bitrate_kbps):
    """Klasördeki tüm videoları tarar, altyazılarla eşleştirir ve belirlenen kelimenin geçtiği yerleri keser."""
    global stop_processing
    stop_processing = False
    
    os.makedirs(output_folder, exist_ok=True)
    total_videos = 0
    total_videos_cut = 0

    # İlk olarak işlenecek toplam video sayısını ve kesilecek video sayısını hesapla
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".mp4"):
            total_videos += 1
            srt_file = os.path.join(folder_path, filename.replace(".mp4", ".srt"))
            if os.path.exists(srt_file):
                timestamps = find_word_in_srt(srt_file, keyword)
                total_videos_cut += len(timestamps)

    current_file_label.config(text=f"Toplam Video: {total_videos}, Kesilecek Video: {total_videos_cut}")
    tk_root.update()

    processed_videos = 0
    processed_cuts = 0

    for filename in os.listdir(folder_path):
        if stop_processing:
            log_message("İşlem durduruldu.")
            current_file_label.config(text="İşlem durduruldu.")
            tk_root.update()
            break
        
        if filename.lower().endswith(".mp4"):
            video_file = os.path.join(folder_path, filename)
            srt_file = os.path.join(folder_path, filename.replace(".mp4", ".srt"))
            
            if not os.path.exists(srt_file):
                log_message(f"❌ {filename} için altyazı dosyası bulunamadı, atlanıyor.")
                continue
            
            current_file_label.config(text=f"PROCESSING VIDEO: {filename} ({processed_videos + 1}/{total_videos})")
            tk_root.update()
            log_message(f"🔍 PROCESSING VIDEO: {filename}")
            timestamps = find_word_in_srt(srt_file, keyword)
            
            if not timestamps:
                log_message(f"⚠️ '{keyword}' kelimesi {filename} içinde bulunamadı.")
                continue
            
            for idx, (start, end) in enumerate(timestamps):
                start_formatted = start.split('.')[0].replace(":", "-")
                end_formatted = end.split('.')[0].replace(":", "-")
                bitrate_mbps = bitrate_kbps // 1000  # Bitrate'i 1000 ile böler
                sanitized_filename = sanitize_filename(f"{os.path.splitext(filename)[0]}_{idx}_{start_formatted}_{end_formatted}_{bitrate_mbps}mbps")
                output_clip = os.path.join(output_folder, sanitized_filename)
                
                cut_video(video_file, start, end, output_clip, bitrate_kbps)
                processed_cuts += 1
                total_videos_label.config(text=f"PROCESSED: {processed_cuts}/{total_videos_cut}")
                tk_root.update()
            processed_videos += 1
    
    if not stop_processing:
        completion_label.config(text="Tüm işlemler tamamlandı.")
    total_videos_label.config(text=f"PROCESSED: {processed_cuts}/{total_videos_cut}")
    start_button.config(bg="lightgreen")  # Change the start button color back to green
    tk_root.update()

def select_folder(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)

def start_processing():
    global stop_processing
    stop_processing = False
    
    # Reset labels
    current_file_label.config(text="PROCESSING: -")
    total_videos_label.config(text="PROCESSED: 0")
    start_button.config(bg="#f44336")  # Change the start button color to red
    tk_root.update()
    
    folder_path = folder_entry.get()
    output_folder = output_entry.get()
    keyword = keyword_entry.get()
    bitrate_kbps = bitrate_entry.get()
    
    if not folder_path or not output_folder or not keyword or not bitrate_kbps:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
        start_button.config(bg="lightgreen")  # Change the start button color back to green
        return
    
    try:
        bitrate_kbps = int(bitrate_kbps)
    except ValueError:
        messagebox.showerror("Hata", "Bitrate değeri geçerli bir sayı olmalıdır!")
        start_button.config(bg="lightgreen")  # Change the start button color back to green
        return
    
    processing_thread = threading.Thread(target=process_videos_in_folder, args=(folder_path, keyword, output_folder, bitrate_kbps))
    processing_thread.start()

def stop_processing():
    global stop_processing
    stop_processing = True

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    tk_root.update()

# Tkinter Arayüzü
tk_root = tk.Tk()
tk_root.title("CutCaption")

video_frame = tk.Frame(tk_root)
video_frame.pack(pady=(5, 10), padx=(10, 10), anchor='w')
tk.Label(video_frame, text="VIDEO:").pack(side=tk.LEFT)
folder_entry = tk.Entry(video_frame, width=50)
folder_entry.pack(side=tk.LEFT, padx=(5, 5))
tk.Button(video_frame, text="Browse", command=lambda: select_folder(folder_entry)).pack(side=tk.LEFT)

output_frame = tk.Frame(tk_root)
output_frame.pack(pady=(5, 10), padx=(10, 10), anchor='w')
tk.Label(output_frame, text="OUTPUT:").pack(side=tk.LEFT)
output_entry = tk.Entry(output_frame, width=50)
output_entry.pack(side=tk.LEFT, padx=(5, 5))
tk.Button(output_frame, text="Browse", command=lambda: select_folder(output_entry)).pack(side=tk.LEFT)

keyword_frame = tk.Frame(tk_root)
keyword_frame.pack(pady=(5, 10), padx=(10, 10), anchor='w')
tk.Label(keyword_frame, text="KELİME:").pack(side=tk.LEFT)
keyword_entry = tk.Entry(keyword_frame, width=50)
keyword_entry.pack(side=tk.LEFT, padx=(5, 5))

bitrate_frame = tk.Frame(tk_root)
bitrate_frame.pack(pady=(5, 10), padx=(10, 10), anchor='w')
tk.Label(bitrate_frame, text="Bitrate (kbps):").pack(side=tk.LEFT)
bitrate_entry = tk.Entry(bitrate_frame, width=50)
bitrate_entry.pack(side=tk.LEFT, padx=(5, 5))

button_frame = tk.Frame(tk_root)
button_frame.pack(pady=(0, 10))
start_button = tk.Button(button_frame, text="START", command=start_processing, bg="lightgreen")
start_button.pack(side=tk.LEFT, padx=(0, 5))
tk.Button(button_frame, text="STOP", command=stop_processing).pack(side=tk.LEFT)

current_file_label = tk.Label(tk_root, text="PROCESSING VIDEO: -")
current_file_label.pack(pady=(10, 5), padx=(10, 10), anchor='w')

total_videos_label = tk.Label(tk_root, text="PROCESSED: 0")
total_videos_label.pack(pady=(0, 10), padx=(10, 10), anchor='w')

log_text = tk.Text(tk_root, height=15, width=80)
log_text.pack(pady=(0, 10), padx=(10, 10), anchor='w')

completion_label = tk.Label(tk_root, text="")
completion_label.pack(pady=(0, 10), padx=(10, 10), anchor='w')

tk_root.mainloop()
