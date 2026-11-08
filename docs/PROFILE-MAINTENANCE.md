# Profil güncelleme rehberi

README'nin üst bölümü çalışma alanlarını ve teknik araçlarını anlatır. Yeni bir proje eklerken bu bölümü yeniden düzenlemek gerekmez.

## Yeni çalışma ekleme

Çalışmayı en yakın başlığın altına ekle:

| Başlık | Kapsam |
| --- | --- |
| Control & robotics | Kontrol, robotik ve mekanik sistemlerle ilgili çalışmalar |
| Embedded & digital | Firmware, mikrodenetleyiciler, VHDL ve FPGA çalışmaları |
| Power Electronics | Dönüştürücüler, sürücüler, güç dağıtımı ve elektronik donanım |

README'deki Engineering work bölümünü aç ve ilgili başlığın altına bir satır ekle. Bir çalışma birden fazla alana dokunuyorsa ana katkının bulunduğu kategoriyi seç. Aynı bağlantıyı birkaç bölümde tekrarlama.

Şu Markdown yapısını kopyalayıp köşeli ayraçlı alanları değiştir:

```markdown
- [Çalışmanın adı](PORTFOLIO_URL) — kısa teknik bağlam
```

Kaynak kod yayımlandığında aynı satırın sonuna `[Source](REPOSITORY_URL)` ekleyebilirsin. Sadece repo varsa çalışma adını doğrudan repoya bağla. Kopyaladığın örnekteki yer tutucuları gerçek ad ve adresle değiştir.

## Devam eden çalışma

Durumu açıklamanın başında belirt: `In progress — ...`. Bitirme projesinin konusu paylaşılabilir hale gelince bir cümleyle problem ve yaklaşımı anlat. Tamamlanmayan özellikleri sonuç gibi yazma.

Ölçüm varsa test koşuluyla birlikte ekle. Örneğin takip hatası, örnekleme hızı veya çıkış dalgalanması ancak ölçüldüğünde yer almalı.

## Yetkinlikleri güncelleme

Çalışma alanlarını README'nin Areas bölümünde tut. Ana araçlar `assets/toolkit.json` dosyasındaki kısa gruplardan üretilir. Bir aracı ekledikten sonra `python scripts/build_toolkit.py` komutuyla açık/koyu ve mobil görselleri yenile. Alternatif metin de otomatik güncellenir. README değişikliklerinden sonra `python scripts/build_static.py` ile statik sürümü eşitle.

Öğrenmeye başladıkların In progress bölümünde, henüz başlamadıkların Interested in exploring bölümünde yer alır. Bu iki bölümde de Areas satırına genel alanları, Tools satırına araçları yaz. Bir aracı kullanmaya başladığında ana araç grubuna taşı. MATLAB alt araçları, IDE veya platform eklentileri için yeni kalem açmana gerek yok. İsimleri kısa tut; uzun konu açıklamaları, yüzde, yıldız veya seviye çubuğu ekleme.

Yeni bir ilgi alanı için ayrı bölüm açmadan önce mevcut üç ana alandan birine uyup uymadığına bak. Kısa ve okunabilir bir başlangıç bölümü koru.

## Yayımlamadan önce

- Proje, portföy ve iletişim bağlantılarını açıp kontrol et.
- GitHub'ın Preview görünümünde başlıkları ve satır aralarını kontrol et.
- Açık ve koyu temada görsellerin okunabildiğini doğrula.
- Dar ekranda yatay taşma olmadığını kontrol et.
- Mezun olduğunda tanıtımdaki öğrenci ifadesini güncelle.

Bu rehberi README'ye kopyalamana gerek yok. README içinde bakım talimatı, HTML yorumu veya boş proje şablonu bulunmamalı.

## Üst görsel ve tipografi

Yeni proje eklemek animasyonu yeniden üretmeyi gerektirmez. Üst görselin zamanlaması, statik sürümü ve yeniden üretim komutları ANIMATION.md içinde. İsim tek kez yazılır; robotun devam eden döngüsü bunu tekrar başlatmaz.

Kimlik ve araç yazıları Bricolage Grotesque ile üretilir. Font ve OFL lisansı assets/fonts içinde bulunur; ziyaretçinin font yüklemesi gerekmez. Araç etiketleri assets/toolkit.json üzerinden değiştirilir. Ardından python scripts/build_toolkit.py ve python scripts/build_static.py komutlarını çalıştır.

JavaScript veya sticky CSS'i README'ye ekleme: GitHub bunları kaldırır. Bu davranışları sadece yerel önizlemeye ekleyip GitHub'da varmış gibi sunma.

## Profile views

The Socials row uses [Komarev](https://github.com/antonkomarev/github-profile-views-counter) with the public username. It counts image requests through GitHub’s proxy, not unique visitors or historical account traffic. Previewing or reloading can affect the count; caching can delay updates. No base offset is added. This widget does not read repositories or contributions, including private activity. Keep the same username parameter to retain the counter.

## Tool modules

Edit `assets/toolkit.json`: each category has a name, line icon, accent and list of tools. The builder wraps individual badges within three desktop columns or two mobile columns. Run `python scripts/build_toolkit.py` after edits. Keep each category to two badge rows; long additions may require a larger module height. Social links are independent linked images in README.md.

## Content and public artwork

`assets/profile.json` owns institution, discipline, status, working areas and learning interests. Edit the status string when graduating; the layout does not change. `assets/learning.json` and `assets/exploring.json` own the open tool lists. Run `python scripts/build_dashboard.py` after changes.

`assets/public-profile.json` is a public-only snapshot. `scripts/refresh_public_profile.py` uses unauthenticated public GitHub endpoints. The contribution circuit maps dates to GitHub activity levels, not commit totals. GitHub's own graph remains the source; private-contribution display must stay off. No private repositories are requested or counted. The optional daily workflow refreshes public artwork after merging to the default branch; it has not run in this draft branch.

Repository cards link to public repositories; they do not change GitHub's native pinned-repository selection. Edit README ordering to curate the card section. Icons are monochrome local vectors from Devicon and Simple Icons (their upstream licenses apply). Product logos unavailable in these sets use a shared circuit symbol. Autodesk and ST/Espressif marks represent their respective tool families. No logo implies endorsement.

The tiny view counter is at the footer. SVG animation failure cannot be detected by README markup once SVG has been selected. The default unanimated frame and reduced-motion sources handle common static cases; the footer Still version remains an explicit alternative.
