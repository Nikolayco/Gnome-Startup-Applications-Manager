# GNOME Başlangıç Uygulamaları Yöneticisi

🌍 **Türkçe | [English](README.md) | [Русский](README.ru.md) | [Български](README.bg.md)**

`systemd --user` altyapısıyla tam kapsamlı bir **Görev Zamanlayıcı** içeren, modern GTK tabanlı GNOME başlangıç uygulama yöneticisi. Tamamen Python ile yazılmıştır — sıfır ek bağımlılık.

Uygulama **sistem dilinizi otomatik olarak algılar** ve Türkçe, İngilizce, Rusça veya Bulgarca olarak açılır.

---

## ✨ Özellikler

### Başlangıç Yöneticisi
- **Gerçek Uygulama İkonları** — `.desktop` dosyasındaki gerçek ikonları gösterir
- **Canlı Durum & Kaynak Kullanımı** — PID takibiyle gerçek zamanlı CPU (%) ve RAM (MB/GB)
- **Çoklu Seçim** — birden fazla uygulamayı aynı anda başlat, durdur veya sil
- **Güvenli Durdurma** — PID dosyaları kullanır; asla yanlış süreci öldürmez
- **Terminal Modu** — scriptleri görünür GNOME Terminal penceresinde çalıştır
- **Başlangıç Gecikmesi** — uygulama başına saniye cinsinden gecikme ayarı

### Görev Zamanlayıcısı (Cron Alternatifi)
- **Aralıklı** — her N dakika / saat / günde bir çalıştır
- **Takvim** — belirli gün ve saatlerde çalıştır (örn. her Pazartesi 09:00)
- **Boot** — sistem açılışında (Lingering ile oturum açmadan arka planda)
- **Login** — oturum açıldığında çalıştır
- **Manuel Tetikleme** — "Şimdi Çalıştır" butonu ile anında test et
- **Lingering Desteği** — Ayarlar'dan tek tıkla `loginctl enable-linger`

### Genel
- **Klavye Kısayolları** — `Ctrl+N`, `Ctrl+E`, `Ctrl+S`, `Ctrl+K`, `Delete`
- **Sistem Çekmecesi (Tray)** — arka planda sessizce çalışır
- **Pencere Hafızası** — boyut ve konum hatırlanır
- **Çoklu Dil** — Türkçe 🇹🇷, İngilizce 🇬🇧, Rusça 🇷🇺, Bulgarca 🇧🇬

---

## 🚀 Kurulum

```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
python3 baslangic-yoneticisi.py
```

**Gereksinimler:** Python 3.8+, GTK 3, systemd

---

*Geliştirici: Nikolayco — Sürüm 1.1*
