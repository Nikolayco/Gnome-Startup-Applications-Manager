# GNOME Başlangıç Uygulamaları Yöneticisi

🌍 **Türkçe | [English](README.md) | [Русский](README.ru.md) | [Български](README.bg.md)**

---

> Hem GNOME başlangıç uygulamalarını yönetebilen hem de gerçek anlamda bir görev zamanlayıcı olarak çalışabilen — belirli aralıklarla, açılışta veya belirli bir saatte script çalıştırabilen — tek bir uygulama aradım. Böyle bir şey bulamadım, o yüzden kendim geliştirdim.

---

`systemd --user` altyapısıyla tam kapsamlı bir **Görev Zamanlayıcı** içeren, modern GTK tabanlı GNOME başlangıç uygulama yöneticisi. Tamamen Python ile yazılmıştır — sıfır ek bağımlılık.

Uygulama **sistem dilinizi otomatik olarak algılar** ve Türkçe, İngilizce, Rusça veya Bulgarca olarak açılır.

---

## ✨ Özellikler

### Başlangıç Yöneticisi
- **Gerçek Uygulama İkonları** — `.desktop` dosyasındaki gerçek ikonları gösterir
- **Canlı Durum & Kaynak Kullanımı** — PID takibiyle gerçek zamanlı CPU (%) ve RAM (MB/GB)
- **Çoklu Seçim** — birden fazla uygulamaìeyı aynı anda başlat, durdur veya sil
- **Güvenli Durdurma** — PID dosyaları kullanır; asla yanlış süreci öldürmez
- **Terminal Modu** — scriptleri görünür GNOME Terminal penceresinde çalıştır
- **Başlangıç Gecikmesi** — uygulama başına saniye cinsinden gecikme ayarı

### Görev Zamanlayıcısı (Cron Alternatifi)
- **Aralıklı** — her N dakika / saat / günde bir çalıştır
- **Takvim** — belirli gün ve saatlerde çalıştır (örn. her Pazartesi 09:00)
- **Boot** — sistem açılışında (Lingering ile oturum açmadan arka planda)
- **Login** — oturum açıldığında çalıştır
- **Manuel Tetikleme** — "Şimdi Çalıştır" butonu ile aninda test et
- **Lingering Desteği** — Ayarlar'dan tek tıkla `loginctl enable-linger`

### Genel
- **Sistem Çekmeçesi (Tray)** — arka planda sessizce çalışır
- **Pencere Hafızası** — boyut ve konum hatırlanır
- **Çoklu Dil** — Türkçe 🇹🇷, İngilizce 🇬🇧, Rusça 🇷🇺, Bulgarca 🇧🇬

---

## ⌨️ Klavye Kısayolları

| Kısayol | İşlev |
|---------|-------|
| `Ctrl + N` | Yeni başlangıç uygulaması ekle |
| `Ctrl + E` | Seçili uygulamaîyı düzenle |
| `Ctrl + S` | Seçili uygulamaîyı başlat |
| `Ctrl + K` | Seçili uygulamaîyı durdur (öldür) |
| `Delete` | Seçili uygulamaîyı sil |
| `Ctrl + F` | Arama kutusuna odaklan |

---

## 🚀 Kurulum

```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git 2>/dev/null || true
cd Gnome-Startup-Applications-Manager
bash install.sh
```

Bu komut uygulamayı `~/.local/bin`'e kurar ve **Uygulama Izgarasına (App Grid)** otomatik olarak ekler.

**Gereksinimler:** Python 3.8+, GTK 3, systemd

---

## 🗑️ Kaldırma

```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git 2>/dev/null || true
cd Gnome-Startup-Applications-Manager
bash uninstall.sh
```

> **Not:** Kendinizin elle eklediği `.desktop` başlangıç uygulamaları bu işlemden etkilenmez. Yalnızca uygulamanın kendi oluşturduğu dosyalar silinir.

---

*Geliştirici: Nikolayco — Sürüm 1.2*
