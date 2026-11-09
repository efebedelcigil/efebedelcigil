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

## Live public data and theme selection

The workflow checks every 15 minutes (GitHub may delay scheduled jobs). It reads native public pins from the public profile page, language byte distributions from public non-fork repositories and contribution-type counts summed only across repositories with `isPrivate == false`. The workflow token is scoped to this public repository; no PAT with private-user access is stored. No private aggregate totals are serialized. Profile views remain a live external counter subject to GitHub image caching.

Both theme images use GitHub's `#gh-dark-mode-only` / `#gh-light-mode-only` suffixes, so manual GitHub appearance overrides the operating-system theme. Responsive/reduced-motion picture sources sit inside each theme variant. This can download both hero variants; GitHub's image/CSS model does not permit custom script selection. Public pins and README rows are regenerated from the same snapshot, with two cards per row and truncated titles/descriptions.

`build_dashboard.py`, `build_readme.py`, `build_toolkit.py` and `build_static.py` rebuild their respective modules. Skills were explicitly deferred. SVG artwork has no cross-image hover/zoom or layout interaction in GitHub README.

## Electrical polish and readable text

The current route uses a closed BFS tour of every active public cell, preserving components. The electric battery filament is self-contained SVG animation. Portfolio copy is “Explore my portfolio”; section headings and main explanatory text use native Markdown so they can be selected. Badge and hero lettering remain image content. The browser's selection highlight cannot be removed through GitHub README styling. Theme preview wrappers remain with the user's explicit acceptance.

Pinned cards use inline images at 49% width instead of a nested table, avoiding native table borders. Language distribution is the sum of GitHub language API byte values per eligible public repository; the snapshot stores per-repository language_sources for audit. It is not skill proficiency, project count or a fabricated engineering-language mix.

## Shared headings and learning layout

All primary section headers come from the same `heading-*` generator. Areas/Tools & methods branches use a smaller common style. TinyML lives in `assets/learning.json` under Methods, while Machine learning remains in `profile.json` under learning_areas. Sensor fusion replaces Sensing. LTspice and Proteus are grouped under Simulation; KiCad and EAGLE under PCB design.

`design_parts.py` provides typography measurement and the restrained category-colored perimeter animation. Static and reduced-motion badge variants share layout and contain no animation. The hero includes institution/status beneath the name; `python scripts/refresh_hero.py` updates lettering using existing embedded raster frames without re-rendering the robot. Working areas uses the earlier card layout; the control diagram is not displayed.

Contribution package tops have bevels and raised side walls. The current route stays at PCB level, behind raised package geometry, and uses copper/orange-only glow. It covers every active date in the public snapshot and is recalculated when the snapshot changes.

Current is drawn at PCB level before package geometry. Opaque chip bodies occlude it; internal windows pulse at the first visit of the moving signal, derived from route arc length. Four-sided contacts make entry and exit visible. It no longer rides across the raised lid.

## Current icon and layout system

All displayed UI icons now come from the bundled Tabler outline collection (MIT, `assets/icons/LICENSE`). `assets/icon-map.json` maps each tool/field to an intentional icon; missing mappings fail rather than showing a default chip. 3D printing uses `stack-3`, representing additive layers rather than an inkjet printer. CAD's visible label is simply CAD; its learning status remains metadata, with SolidWorks/Fusion in progress.

Branch categories match the Tools category format. Junctions point to group labels, with consistent grid alignment. Border highlights all use normalized pathLength 100, phase zero and an eight-second period; lead/trail lengths are scaled from actual rounded perimeter. Each SVG has its own image clock, so cross-image loading can introduce a small start offset, but there are no intentional phase offsets.

Main headings are custom display blocks rather than Markdown heading tags, preventing GitHub's automatic heading-link chain. Two named theme targets at the hero support the themed Back to top control. A sticky/scroll-triggered floating control cannot be implemented in README; this is a footer anchor. Pin languages come from each public pinned repository's language endpoint, not just primaryLanguage. Footer colors use explicit theme variants, with a neutral counter-label portion supplied by the external counter service.

Final icon preference: recognized tool/vendor vector marks are restored from brand-map.json, with preserved negative detail. Tabler is used for category/field/UI symbols and explicitly mapped tools without a bundled brand mark. There is no default fallback. EAGLE restores the earlier Autodesk-family mark; GND is assigned to Circuit design. 3D printing remains additive layers.
