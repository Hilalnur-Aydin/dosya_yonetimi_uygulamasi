# 📁 Dosya Yükleme ve Yönetimi Uygulaması

Kullanıcıların hesap oluşturabildiği, giriş yapabildiği, dosya yükleyip indirebildiği basit bir web uygulamasıdır. Bu proje, dosya yönetimi sistemlerinin temel işleyişini öğrenmek amacıyla Flask kullanılarak geliştirilmiştir.

## 🚀 Özellikler

- Kullanıcı kayıt ve giriş sistemi
- Güvenli dosya yükleme
- Yüklenen dosyaları listeleme ve indirme
- Bootstrap ile modern ve kullanıcı dostu arayüz

## 🛠 Kullanılan Teknolojiler

- **Python** – Uygulama mantığı ve sunucu tarafı işlemler için
- **Flask** – Hafif web framework’ü
- **HTML/CSS** – Arayüz tasarımı
- **Bootstrap** – Responsive ve şık tasarım için
- **SQLite** – Hafif veritabanı sistemi
- **Git & GitHub** – Versiyon kontrolü ve proje paylaşımı

## 📁 Proje Yapısı

dosya_yonetimi_uygulamasi/
│
├── static/ # Statik dosyalar
│ ├── style.css
├── templates/ # HTML şablonları
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ └── upload.html
│
├── uploads/        # Yüklenen dosyaların saklandığı klasör (otomatik oluşur)
├── app.py          # Flask uygulamasının ana dosyası
├── database.db     # SQLite veritabanı dosyası
├── .git/           # Git versiyon kontrol klasörü
├── __pycache__/    # Python derlenmiş dosyaları (otomatik oluşur)
├── instance/       # Flask instance klasörü (config için olabilir)
└── venv/ 


## Kurulum ve Çalıştırma

1. Sanal ortam oluşturun ve aktif edin (opsiyonel ama önerilir):
    ```
    python -m venv venv
    venv\Scripts\activate   # Windows için
    source venv/bin/activate  # Mac/Linux için
    ```
2. Gerekli paketleri yükleyin:
    ```
    pip install flask
    ```
3. Uygulamayı başlatın:
    ```
    python app.py
    ```
4. Tarayıcıdan `http://localhost:5000` adresine gidin.

## Kullanım

- Dosya yükleme, listeleme ve yönetme işlemleri yapılabilir.
- Bootstrap ile kullanıcı arayüzü geliştirilmiştir.

---

**Not:** Proje basit bir dosya yönetimi uygulamasıdır ve eğitim amaçlı hazırlanmıştır.
