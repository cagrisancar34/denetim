# Spor İstanbul Tesis Standartları Denetim Uygulaması

Bu proje, Spor İstanbul tesislerinde yapılan denetimlerin dijital olarak kaydedilmesi, puanlanması ve raporlanması için geliştirilmiş bir Flask tabanlı web uygulamasıdır.

## Klasör ve Dosya Yapısı

```
/denetim
├── app.py                  # Ana Flask uygulama dosyası
├── data.json               # Kategori ve soruların JSON formatında tutulduğu dosya
├── denetimler.json         # Yapılan denetimlerin kayıtlarının tutulduğu dosya
├── requirements.txt        # Gerekli Python paketleri
├── TESİS STANDARTLARI DENETİM TABLOSU LV 08032023.xlsx # Soru ve kategorilerin kaynağı (Excel)
└── templates/
    ├── form.html           # Denetim formu arayüzü
    ├── index.html          # Ana sayfa
    ├── kategori.html       # Kategori ve soru ekleme arayüzü
    ├── submit.html         # Form gönderildikten sonraki özet sayfası
    └── tesis_karnesi.html  # Tesis bazlı skor ve rapor sayfası
```

## Temel Akış

1. **Kategori ve Soru Yönetimi**
   - `data.json` dosyasında kategoriler ve sorular tutulur.
   - Yeni kategori ve soru ekleme işlemleri `kategori.html` üzerinden yapılır.
   - Kategoriler ve sorular dinamik olarak formda gösterilir.

2. **Denetim Formu**
   - `form.html` üzerinden tesis, tarih, denetim yapan kişi ve her kategoriye ait sorular yanıtlanır.
   - Her soru için "Evet", "Hayır" veya "Yok" seçilebilir. Açıklama alanı isteğe bağlıdır.
   - Form gönderildiğinde yanıtlar `denetimler.json` dosyasına kaydedilir.

3. **Puanlama ve Raporlama**
   - Puanlama algoritması:
     - "Evet": +1 puan ve max skora eklenir
     - "Hayır": sadece max skora eklenir
     - "Yok": puan ve max skora eklenmez
   - Sonuçlar ve kategori bazlı skorlar `submit.html` ve `tesis_karnesi.html` üzerinden görüntülenir.

## Geliştiriciye Notlar

- Tüm veri işlemleri (kategori, soru, denetim kaydı) JSON dosyaları üzerinden yapılır.
- Yeni kategori/soru eklemek için backend ve frontend akışına dikkat edin. Kategoriler ve sorular dinamik olarak yüklenir.
- Puanlama algoritmasını bozmadan yeni özellikler ekleyebilirsiniz. Algoritma `app.py` içinde `calculate_score` ve `get_category_scores` fonksiyonlarında tanımlıdır.
- Arayüz Bootstrap ile tasarlanmıştır, responsive ve modern bir yapıdadır.
- Açıklama alanları isteğe bağlıdır, zorunlu değildir.
- Kodda ve veri dosyalarında Türkçe karakterler kullanılmaktadır, encoding ayarlarına dikkat edin.

## Kurulum

1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
2. Uygulamayı başlatın:
   ```bash
   python app.py
   ```
3. Tarayıcıdan `http://127.0.0.1:5000` adresine giderek uygulamayı kullanabilirsiniz.

## Geliştirme
- Kod modüler hale getirilmiştir: Veri işlemleri `data_utils.py`, skor hesaplama ve analiz fonksiyonları `score_utils.py` dosyalarına taşınmıştır.
- Fonksiyonlarda hata yönetimi (try-except) uygulanmıştır.
- Otomatik testler için örnek dosya: `test_score_utils.py` (unittest ile çalıştırılır).
- Arayüz Bootstrap ile responsive ve modern yapıdadır.
- Güvenlik ve performans için girdi doğrulama ve hata yönetimi eklenmiştir.
- Yeni özellik eklerken mevcut veri yapısını ve fonksiyonları bozmadan ilerleyin.
- Tüm HTML dosyaları `templates/` klasöründe bulunur.
- Backend kodu tek dosyada (`app.py`) tutulmaktaydı, artık modüller kullanılmaktadır.

## İyileştirme Önerileri
1. Kodun modülerleştirilmesi
2. Hata ve istisna yönetimi
3. Otomatik testler
4. Modern ve kullanıcı dostu arayüz
5. Performans optimizasyonu
6. Güvenlik önlemleri
7. Dokümantasyon
8. API desteği
9. Versiyon kontrolü

## İletişim
Herhangi bir sorunuz veya katkınız için proje yöneticisiyle iletişime geçebilirsiniz.
