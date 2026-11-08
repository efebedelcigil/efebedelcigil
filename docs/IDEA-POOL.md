# Kişisel robotik atölyesi

Profilin üst görseli, Efe'nin kontrol ve robotik odağını küçük bir atölye sahnesiyle anlatır. Robot kol sahnede gerçekten bir iş yapar; isim, elektronik parçalar ve küçük ekran aynı çalışma alanının parçalarıdır. Görsel dil, Blender estetiğinde hacimli parçalar, gölgeli materyaller ve ölçülü hareket üzerine kurulur.

## Birlikte uygulanacak çekirdek

- **Çalışan robot kol:** Kısa bir kalibrasyon hareketinden sonra masadaki görevlerine geçer. Eklem hareketleri ve tutucunun açılıp kapanması yapılan işe karşılık gelir.
- **İsimle etkileşim:** Kol, isimde hizası bozulan bir parçayı düzeltir. İsim okunabilir kalır; hareket kişisel bir ayrıntı oluşturur.
- **Katkı PCB'si:** Kol küçük parçaları bir devre kartına yerleştirir. Kart, katkı fikrini elektronik üretimiyle birleştirir; prototipteki yerleşim gerçek GitHub etkinliği olarak sunulmaz.
- **Okuyucuya kısa bakış:** Kol, bileşeni yerleştirdikten sonra inceleme kamerasını öne uzatır ve yaklaşık yarım saniye izleyiciye döner. Küçük üçgen tarama izi, işine dönmeden önce kısa bir selam gibi görünür. Ziyaretçiyi gerçekten algıladığı iddia edilmez.
- **Mini ekran:** Kalibrasyon ve yerleştirme gibi o anki göreve eşlik eder. Robotun hareketiyle aynı hikâyeyi anlatır.
- **Kontrol cevabı:** Mini ekranda referans ve sistem cevabı birlikte görünür. Kol ayar düğmesini çevirdiğinde salınımlı örnek cevap yerleşir. Bu, sahnenin hareketini anlatır; ölçülmüş proje sonucu değildir.
- **Tek sahne ve kısa döngü:** Bu anlar ayrı animasyon kutuları yerine aynı atölyede birbirini izler. Döngü 12 saniyedir; isim ve içerik ilk kareden itibaren okunur. Bileşen takıldıktan sonra kol tarafından tekrar tepsiye taşınır. Döngü başa dönerken nesneler ve kolun konumu tutarlı kalır.
- **Gerçek şeffaflık:** Arka plan saydamdır. Parçalar ve gölgeler açık ve koyu GitHub temasında birlikte kontrol edilir; görselin çevresinde sabit renkli bir panel bulunmaz.

Prototip, Blender'da modellenip önceden hesaplanmış şeffaf WebP animasyonu olarak README'ye gömülür. GitHub içinde özel JavaScript çalıştırmaz. Sayfa kaydırmasına veya sürüklemeye tepki veriyormuş gibi gerçek bir etkileşim vaat etmez; sahnedeki hareketler animasyonun kendi zaman çizelgesine aittir.

## Sonraki aşama

**Gerçek katkı verisi:** İlk sürümde PCB'nin 28 pedi, herkese açık katkı takvimindeki son 28 günün aktivite seviyelerini taşır. Veri kaynağı ve son güncelleme tarihi `assets/workbench-data.json` içinde kayıtlıdır. Yenileme ve yeniden render adımları `docs/ANIMATION.md` içinde anlatılır. Düzenli otomatik render henüz etkin değildir.

**Ziyaretçi oylaması:** Ziyaretçiler robotun sonraki görevini veya bir sonraki atölye çalışmasını seçebilir. Oy verme, README'den bağlantıyla açılan bir sayfada yürütülür. Sonuçlar daha sonra sahnenin yeniden üretilmesine yansıtılabilir; mevcut prototip canlı oy toplamaz.

## Havuzdaki diğer hareketler

| Fikir | Kullanım |
| --- | --- |
| Kendi kendini kalibre etme | Ayar düğmesi ve kontrol cevabıyla ilk döngüde var. |
| İsim atölyesi | EVB isim plakasıyla ilk döngüde var; tam isim sürekli okunur. |
| Deney masası | Bileşen takma/çıkarma, PCB ve geri besleme ekranıyla ilk döngüde var. |
| Kendi kendinin teknisyeni | Kontrol paneli açma ve uç değiştirme, ileride mevcut hareketlerden birinin yerine geçebilir. |
| Zamanla değişen masa | Yeni çalışmalar eklendikçe bir sensör veya motor eklenebilir; her döngüye daha fazla iş yığılmaz. |
| Küçük sürprizler | Düşen parçayı yakalama veya isim noktasını düzeltme, sonraki alternatif döngüler için tutuluyor. |
| Çizgiyi çekip bölümü açma | Ayrı etkileşimli sahne için uygun; gerçek GitHub scrollbar'ına müdahale edilemez. |

Snake, Pac-Man, bonsai ve bağımsız istatistik panelleri araştırma referansları olarak kaldı. Aynı profile eklenmediler; katkı fikri PCB sahnesine uyarlandı.

## Profil içeriğiyle ilişkisi

Animasyon, kısa tanıtımı ve portföy bağlantılarını destekler. İsim ve teknik odak erişilebilir metinde de yer alır. Areas, Tools, In progress ve Interested in exploring bölümlerindeki seçili alanlar, araçlar ve seviyeler bu görsel değişikliğiyle değişmez. Sahnedeki bir nesne, tek başına yeni bir yetkinlik iddiası sayılmaz.

Görsel varlıkların dosya düzeni ve yeniden üretim adımları `docs/ANIMATION.md` içinde bulunur.
