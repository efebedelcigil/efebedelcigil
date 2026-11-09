# Profili nasıl düzenlerim?

Bu profil modülerdir. Metin ve araçları aşağıdaki JSON dosyalarından değiştir; README ve SVG dosyaları otomatik üretilir. JSON içinde çift tırnak kullan, son elemandan sonra virgül koyma.

## En kolay yol: GitHub üzerinden

1. İlgili dosyayı aç, kalem simgesine bas, içeriği değiştir ve kaydet.
2. Actions → Public profile artwork çalışmasını takip et. Gerekirse Run workflow ile elle başlat.
3. İşlem README ve görselleri yeniler. GitHub önbelleği nedeniyle görüntü biraz geç değişebilir.

## Hangi dosyada ne var?

| Değiştirmek istediğin şey | Dosya |
|---|---|
| Bölüm, üniversite, öğrencilik/mezuniyet durumu, portföy adresi | assets/profile.json |
| Working areas | profile.json içindeki areas; ilk iki alan ana başlığı oluşturur |
| In progress alanları | learning_areas ve learning_area_groups |
| Interested in exploring alanları | exploring_areas ve exploring_area_groups |
| Tools kategorileri ve araçlar | assets/toolkit.json |
| Öğrenilen araç/yöntemler | assets/learning.json |
| Keşfedilecek araç/yöntemler | assets/exploring.json |
| Araçların marka logoları | assets/brand-map.json ve assets/logos/ |
| Diğer ikon eşlemeleri | assets/icon-map.json ve assets/icons/ |

Alan listesi kısa açıklama/erişilebilirlik metnidir; aynı alanın görsel kartı ilgili *_area_groups listesindedir. Alan eklerken ikisini de güncelle.

## Örnek: mezun olduğumda

profile.json içinde yalnız status değerini değiştir: örneğin “Electrical & Electronics Engineer”. Tasarım değişmez; isim altındaki satır yeniden üretilir.

## Araç eklemek veya taşımak

İlgili kategorinin tools listesine adı ekle. Örneğin Programming listesine yeni bir dil ekleyebilirsin. Bir aracı öğrenme bölümünden Tools’a taşırken eski listeden çıkar, toolkit.json içindeki uygun kategoriye ekle.

Yeni kategori örneği:

```json
{"name":"Robotics","tools":["ROS 2","Gazebo"]}
```

Tools kategorilerinde ayrıca color bulunur: blue, teal veya warm. Kategori adı ve eklediğin araç için ikon eşlemesi de bulunmalı. İkonu eksik öğeler için rastgele bir default ikon üretmeyiz; eksik eşlemeyi tamamla. İkon adıyla araç adının yazımı birebir aynı olmalı.

## Otomatik gelen veriler

Pinned repositories GitHub profilindeki gerçek pinleri ve sıralarını izler. Pin eklemek için profilindeki Customize your pins bölümünü kullan. Kart açıklaması repodaki Description alanından, dil listesi GitHub API’den gelir; sığmayan metin kısaltılır.

Katkı devresi, tarih aralığı, public activity ve dil dağılımı GitHub’dan yenilenir. assets/public-profile.json üretilmiş veri dosyasıdır; elle değiştirme. Özel repolar dahil edilmez. Dil grafiği yetkinlik değil, public kaynak kodu bayt dağılımıdır. Kontrol 15 dakikada bir yapılır; Actions/önbellek gecikmesi olabilir.

## Tasarımı değiştirmek istersem

- scripts/design_parts.py: ortak yazı ölçüleri, küçük kartlar ve haleler.
- scripts/build_dashboard.py: bölüm başlıkları, Working areas, öğrenme blokları, PCB ve repo kartları.
- scripts/build_toolkit.py: ana Tools düzeni; satırdaki L çerçeveleri eşit yüksekliğe uzar, kartlar üstte kalır.
- scripts/build_hero.py: isim ve robot yerleşimi. refresh_hero.py mevcut karelerle günceller; yeni robot hareketi için render gerekir.
- scripts/build_readme.py: sayfa sırası, sosyal bağlantılar ve footer. GitHub/LinkedIn adreslerini buradan değiştir.

README.md, docs/STATIC.md ve assets/*.svg üzerinde kalıcı elle düzenleme yapma; sonraki otomasyon bunları yeniden yazar. Düzeni değiştirmek için üretici scripti değiştir. SVG tema bağlantılarındaki #gh-dark-mode-only / #gh-light-mode-only parçalarını silme.

## Bilgisayarda üretmek istersem

Python 3.12+ ile:

```sh
python -m pip install fonttools pillow
python scripts/build_dashboard.py
python scripts/build_toolkit.py
python scripts/refresh_hero.py
python scripts/build_readme.py
python scripts/build_static.py
```

Robot kareleri değişmediği sürece Blender gerekmez. Sosyal medya, pin ve portföy bağlantılarını değiştirdikten sonra tıklayarak kontrol et. Uzun araç adlarında mobil görünümü de kontrol et.

## Bilinen sınırlar ve gelecek işler

GitHub README özel hover/zoom, sabit navbar veya kaydırınca beliren bir düğme çalıştırmaz. Back to top footer bağlantısıdır. Still version animasyonsuz alternatiftir. Custom profile views sayacı gelecekte, gerçek bir sayım servisiyle yapılacak; mevcut sayfadan kaldırılmıştır.
