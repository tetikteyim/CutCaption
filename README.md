# CutCaption - Video Cutting Automation Tool

CutCaption is a Python-based desktop application that automates the process of cutting video segments based on subtitle keyword searches. The tool searches for specific words in subtitle files (.srt) and extracts the corresponding video segments, making it ideal for content creators and video editors.

## Features

- 🎯 Search for specific keywords in subtitle files
- ✂️ Automatically cut video segments based on keyword occurrences
- 🎬 Process multiple video files in batch
- 📁 Custom input and output folder selection
- 🔧 Adjustable video bitrate settings
- 🎨 User-friendly graphical interface
- 🔄 Real-time processing status updates
- 🛑 Ability to stop processing at any time
- 🎭 Smart filename sanitization (handles Turkish characters)
- ⚡ Efficient video processing using FFmpeg

## Requirements

- Python 3.x
- FFmpeg installed and accessible from system PATH
- Required Python packages:
  - pysrt
  - tkinter (usually comes with Python)

2. In the application interface:
   - **VIDEO**: Select the folder containing your video files and corresponding .srt files
   - **OUTPUT**: Choose the destination folder for cut video segments
   - **KELİME**: Enter the keyword to search for in subtitles
   - **Bitrate**: Specify the desired output video bitrate in kbps

3. Click "START" to begin processing
   - Monitor progress in real-time through the interface
   - Use "STOP" button if you need to interrupt the process

## File Naming Convention

Output files follow this format:
```
original_filename_index_starttime_endtime_bitratevalue_mbps.mp4
```

Example: `video_0_00-05-30_00-05-35_2mbps.mp4`

## Technical Details

- Video segments include 1-second padding before and after the keyword occurrence
- Supports both Turkish and English characters in filenames
- Video encoding uses H.264 codec with AAC audio
- Audio bitrate is fixed at 128k
- Automatically handles special characters in filenames
- Preserves video quality while optimizing file size

## Version History

The tool has evolved through multiple versions, with key improvements including:
- v8.2: Real-time terminal output display in GUI
- v8.1: Improved filename format with bitrate information
- v8.0: Enhanced user interface
- v7.x: Added GUI and various quality-of-life improvements
- v6.x: Improved file handling and Turkish character support
- v5.0: Enhanced filename sanitization
- v4.0: Added timecode to filenames
- v3.0: Implemented custom output folder support
- v2.0: Initial subtitle parsing implementation

## Error Handling

The application includes robust error handling for common issues:
- Missing subtitle files
- Invalid video files
- FFmpeg processing errors
- Invalid bitrate values
- File access permissions

## Contributing

Feel free to fork this repository and submit pull requests for any improvements you'd like to add.

## License

This project is licensed under the MIT license. See [LICENSE] for details.

## Contact

tetikteyim - [GitHub Profile](https://github.com/tetikteyim)

Project Link: [https://github.com/tetikteyim/cutcaption]

--------------------------------------------------------------------------

# CutCaption - Video Kesme Otomasyonu

CutCaption, altyazılardaki anahtar kelime aramalarına dayalı video kesme işlemlerini otomatikleştiren Python tabanlı bir masaüstü uygulamasıdır. Araç, altyazı dosyalarında (.srt) belirli kelimeleri arar ve ilgili video bölümlerini çıkarır, bu da içerik üreticileri ve video editörleri için idealdir.

## Özellikler

- 🎯 Altyazı dosyalarında belirli kelimeleri arama
- ✂️ Kelime geçen yerlerde otomatik video kesme
- 🎬 Toplu video dosyası işleme
- 📁 Özel giriş ve çıkış klasörü seçimi
- 🔧 Ayarlanabilir video bit hızı
- 🎨 Kullanıcı dostu grafiksel arayüz
- 🔄 Gerçek zamanlı işlem durum güncellemeleri
- 🛑 İşlemi istediğiniz zaman durdurabilme
- 🎭 Akıllı dosya adı düzenleme (Türkçe karakterleri destekler)
- ⚡ FFmpeg kullanarak verimli video işleme

## Gereksinimler

- Python 3.x
- FFmpeg kurulu ve sistem PATH'inde erişilebilir olmalı
- Gerekli Python paketleri:
  - pysrt
  - tkinter (genellikle Python ile birlikte gelir)

2. Uygulama arayüzünde:
   - **VIDEO**: Video dosyalarınızın ve ilgili .srt dosyalarının bulunduğu klasörü seçin
   - **OUTPUT**: Kesilen video bölümlerinin kaydedileceği hedef klasörü seçin
   - **KELİME**: Altyazılarda aranacak kelimeyi girin
   - **Bitrate**: İstenen çıktı video bit hızını kbps cinsinden belirtin

3. İşlemi başlatmak için "START" düğmesine tıklayın
   - İlerlemeyi arayüzden gerçek zamanlı olarak takip edin
   - Gerekirse "STOP" düğmesini kullanarak işlemi durdurun

## Dosya Adlandırma Kuralı

Çıktı dosyaları şu formatı takip eder:
```
orijinal_dosyaadi_index_baslangiczamani_bitiszamani_bitratedegeri_mbps.mp4
```

Örnek: `video_0_00-05-30_00-05-35_2mbps.mp4`

## Teknik Detaylar

- Video bölümlerine kelimenin geçtiği yerden önce ve sonra 1'er saniye eklenir
- Dosya adlarında hem Türkçe hem İngilizce karakterleri destekler
- Video kodlama için H.264 codec ve AAC ses kullanır
- Ses bit hızı 128k olarak sabittir
- Dosya adlarındaki özel karakterleri otomatik olarak düzenler
- Video kalitesini korurken dosya boyutunu optimize eder

## Fonksiyonlar ve Açıklamaları

### replace_turkish_chars(text)
Altyazı dosyasındaki Türkçe karakterleri İngilizce eşdeğerlerine çevirir ve küçük harfe dönüştürür.

### sanitize_filename(filename)
Altyazı dosya adındaki yasaklı karakterleri temizler ve uzantıyı ekler.

### find_word_in_srt(srt_file, keyword)
Altyazı dosyasında belirli bir kelimeyi bulup başlangıç ve bitiş zamanlarını döndürür.

### adjust_time(time_str, delta_seconds)
Verilen zaman stringine belirtilen saniye ekler veya çıkarır.

### cut_video(video_file, start_time, end_time, output_file, bitrate_kbps)
FFmpeg kullanarak videoyu belirli zaman aralığında keser ve hataları yakalar.

### process_videos_in_folder(folder_path, keyword, output_folder, bitrate_kbps)
Klasördeki tüm videoları tarar, altyazılarla eşleştirir ve belirlenen kelimenin geçtiği yerleri keser.

## Arayüz Bileşenleri

- **Video Frame**: Video dosyalarının bulunduğu klasörü seçmek için kullanılır
- **Output Frame**: Kesilen videoların kaydedileceği klasörü seçmek için kullanılır
- **Keyword Frame**: Aranacak kelimeyi girmek için kullanılır
- **Bitrate Frame**: Video bit hızını ayarlamak için kullanılır
- **Button Frame**: START ve STOP düğmelerini içerir
- **Progress Labels**: İşlem durumunu gösteren etiketler
- **Log Text**: İşlem detaylarını gösteren metin alanı

## Sürüm Geçmişi

### Version 8.2
- Terminal çıktıları anlık olarak arayüzde gösterilecek
- İşlemler tamamlandığında çıkan mesaj ana arayüzde görünecek
- İşlem bitti uyarı penceresi kaldırıldı

### Version 8.1
- Dosya ismine bitrate eklendi
- Timecode kısaltıldı (sadece saat, dakika ve saniye)
- Bitrate değeri 1000 ile bölünerek mbps olarak belirtildi

### Version 8.0
- Arayüz düzenlemeleri yapıldı

### Version 7.7
- Toplam video ve kesilecek video sayısı gösterimi eklendi
- İşlem durumu güncellemeleri iyileştirildi
- Start düğmesi renk değişimi özelliği eklendi

### Version 7.6
- Genel iyileştirmeler yapıldı

### Version 7.5
- Bitrate ayarı kbps olarak girilecek şekilde düzenlendi

### Version 7.4
- Arayüze bitrate ayarı eklendi

### Version 7.3
- Kesilen videolara 1'er saniye ekleme özelliği getirildi

### Version 7.2
- Arayüzdeki bilgilerin yenileme hataları düzeltildi

### Version 7.1
- İşlenen dosya ve kesilen video sayısı gösterimi eklendi

### Version 7.0
- Grafiksel kullanıcı arayüzü eklendi

### Version 6.2
- FFmpeg komutları ve dosya ismi düzenleme iyileştirildi
- Hata yakalama mekanizması geliştirildi
- Detaylı log sistemi eklendi

### Version 6.1
- Dosya isimlendirme iyileştirildi
- Hata yakalama geliştirmeleri yapıldı
- FFmpeg komutları optimize edildi

### Version 6.0
- Türkçe karakterleri İngilizce karşılığına çeviren özellik eklendi

### Version 5.0
- Özel karakterlerin _ ile değiştirilmesi eklendi

### Version 4.0
- Dosya isimlerine timecode eklendi

### Version 3.0
- Kesilen videoları belirlenen OUTPUT klasörüne kaydetme özelliği

### Version 2.0
- SRT dosyasından kelime arama özelliği eklendi

## Hata Yönetimi

Uygulama aşağıdaki durumlar için hata yönetimi içerir:
- Eksik altyazı dosyaları
- Geçersiz video dosyaları
- FFmpeg işleme hataları
- Geçersiz bit hızı değerleri
- Dosya erişim izinleri

## Bilinen Sınırlamalar

- Video ve altyazı dosyaları aynı klasörde ve aynı isim ile bulunmalıdır
- Altyazı dosyaları .srt formatında olmalıdır
- Video dosyaları .mp4 formatında olmalıdır
- İşlem sırasında yeterli disk alanı gereklidir

## Katkıda Bulunma

1. Bu projeyi fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Dalınıza push yapın (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

## İletişim

tetikteyim - [GitHub Profile](https://github.com/tetikteyim)

Proje Linki: [https://github.com/tetikteyim/cutcaption]
