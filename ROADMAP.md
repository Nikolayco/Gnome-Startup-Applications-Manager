# Gelecek Planları ve Geliştirme Yol Haritası (Roadmap)

Bu proje aktif olarak geliştirilmektedir. Aşağıdaki özellikler öncelik sırasına göre projeye eklenecektir:

## 1. Güvenilirlik / Çekirdek Mantık
- [x] **PID Tabanlı Süreç Takibi:** Uygulamaların ve scriptlerin durumunu isimden (string) ziyade gerçek İşlem Kimliği (PID) ile takip etmek (Yanlış uygulamanın durdurulmasını %100 engeller).
- [~] **Wayland Desteği:** (İleri bir sürüme ertelendi) `xdotool` kısıtlamalarını aşmak için GNOME-Shell D-Bus eklentisi veya `wlrctl` gibi modern Wayland alternatifleri ile "Terminali Gizle (Minimize)" özelliğini Wayland'e taşımak.

## 2. Kullanılabilirlik ve Arayüz
- [~] **Sürükle & Bırak Sıralama:** (İptal edildi - Alfabetik sıralama yeterli görüldü) Başlangıç uygulamalarının çalışma sırasını görsel olarak sürükle-bırak yöntemiyle ayarlama.
- [~] **Profil Sistemi:** (İptal edildi) "İş Modu", "Oyun Modu" gibi gruplar oluşturup tek tıkla farklı uygulama setlerini topluca açıp kapatabilme.
- [x] **Gerçek .desktop İkonları:** Jenerik terminal ikonları yerine, uygulamanın kendi orjinal ikonunu (örn. Chrome, Firefox) listede gösterebilme.
- [x] **Çoklu Seçim:** Birden fazla uygulamayı aynı anda seçip topluca aktif/pasif yapma veya silme.
- [x] **Klavye Kısayolları:** Hızlı kullanım için arayüzde klavye kısayolları (Örn: Ctrl+N Yeni Ekle, Delete Sil vb.).

## 3. Güçlü Kullanıcı (Power User) Özellikleri
- [ ] **Kaynak Tüketimi Gösterimi:** Her uygulamanın o anki CPU/RAM kullanımını arayüzde gösterme.
- [x] **Log (Kayıt) Paneli:** Scriptlerin arka planda ürettiği çıktıları (stdout/stderr) doğrudan arayüzdeki bir sekmeden canlı okuyabilme (Debug için).
- [ ] **Çökme Bildirimleri:** Beklenmedik şekilde kapanan scriptler için masaüstü bildirimi (Notification) gösterme.
- [ ] **Şablon Kütüphanesi:** Sık kullanılan başlangıç scriptleri için (VPN bağlan, Sistem Temizle vb.) hazır kod şablonları.
- [ ] **Systemd --user Entegrasyonu:** Gelişmiş servis yönetimi ve log okuma işlemleri için systemd servislerini yönetebilme.
