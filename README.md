# YTÜ Blockchain Slides

Kulübün tüm sunumlarını **tek bir marka tasarım sisteminden** üreten Claude Code
skill'i. Ders anlatımı, etkinlik duyurusu, sponsor sunumu, hackathon deck'i —
hepsi aynı görünür.

Çıktı bağımlılıksız tek bir HTML dosyasıdır: fontlar ve görseller base64 gömülü,
ağ bağlantısı gerekmez. Tarayıcıda açılır, projeksiyonda 16:9 kalır, PDF'e
aktarılabilir.

> [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)
> forku. Orijinal skill her deck için 34 şablon arasından stil seçtiriyordu;
> bu sürümde şablonlar kaldırıldı ve yerine tek, kilitli bir sistem kondu.

## Hızlı bakış

Sistemin tamamını görmek için tarayıcıda aç:

```
ytu-brand/components.html
```

Beş slayt arketipi, 18 bileşen ve tüm tokenlar gerçek 1920×1080 ölçeğinde
orada.

## Kullanım

Claude Code içinde kulüp için bir sunum iste. Skill sırayla:

1. Amaç, uzunluk, içerik ve yoğunluk sorar. **Stil sormaz** — stil sabittir.
2. Slayt planını onaya sunar.
3. Tek dosya HTML üretir, tarayıcıda açar.
4. İstersen Vercel'e dağıtır ya da PDF'e aktarır.

Görsel vereceksen dither'dan geçirilir; işlenmemiş fotoğraf kullanılmaz.

## Depo yapısı

```
ytu-brand/
├── design.md            Tasarım sisteminin anayasası — üretimden önce okunur
├── brand.src.css        Kaynak stil dosyası (elle düzenlenen)
├── brand.css            ÜRETİLMİŞ — fontlar base64 gömülü, deck'e kopyalanır
├── components.src.html  Galeri kaynağı
├── components.html      ÜRETİLMİŞ — canlı bileşen galerisi
├── fonts/               EAS VHS TR (yamalı) + Clash Grotesk
├── assets/              Logo ve dither'lanmış görseller
└── tools/
    ├── patch-eas-vhs.py     Fonta Türkçe glifleri ve tabular rakamları ekler
    ├── build-brand-css.py   brand.src.css + fontlar -> brand.css
    ├── build-gallery.py     components.src.html + varlıklar -> components.html
    └── dither.py            Fotoğrafı 1-bit marka görseline çevirir

SKILL.md              Skill akışı (Phase 0-6)
html-template.md      HTML iskeleti ve JS davranışı
viewport-base.css     Sabit sahne CSS'i — her deck'e kopyalanır
scripts/              PPTX çıkarma, Vercel dağıtımı, PDF aktarımı
```

## Tasarım sistemi özeti

| | |
|---|---|
| Yüzeyler | `#0A0A0C` void · `#0E6CFF` signal · `#000560` deep |
| Fontlar | EAS VHS TR (display) · Clash Grotesk (gövde) |
| Izgara | 24px blok — logonun 12.494 birimlik modülünden türetildi |
| Sahne | 1920×1080 sabit, tek transform ile ölçeklenir |
| İmza öğeleri | Film grain · 1-bit dither görsel · köşeli etiket · mavi vurgu bandı |

Ayrıntı ve gerekçeler: [`ytu-brand/design.md`](ytu-brand/design.md).

## Üretilmiş dosyaları yeniden kurma

`brand.css` ve `components.html` üretilmiş dosyalardır; elle düzenlenmez.
Kaynak değiştiğinde:

```bash
cd ytu-brand
python tools/build-brand-css.py    # brand.src.css + fonts -> brand.css
python tools/build-gallery.py      # components.src.html + assets -> components.html
```

Font dosyası değişirse önce yamayı çalıştır:

```bash
python tools/patch-eas-vhs.py <orijinal-eas-vhs.ttf> fonts/eas-vhs-tr.ttf
```

Bağımlılık: `pip install fonttools brotli Pillow`

## Font notu

`fonts/eas-vhs-tr.woff2` yamalanmış bir dosyadır. Orijinal EAS VHS'te **Ğ, İ,
Ş, ğ, ş glifleri yoktu**; marka kitindeki eski afişlerde "BAŞVURU" yerine
"BASVURU" yazmasının sebebi budur. Ayrıca rakamlar üç farklı genişlikteydi, bu
da sayfa sayacında ve tablo sütunlarında kaymaya yol açıyordu.

`tools/patch-eas-vhs.py` eksik beş glifi fontun kendi yarım-piksel ızgarasına
(120.5 birim) oturacak şekilde üretir ve rakamları tek genişliğe eşitler.

Ayrıca deck'lerde `<html lang="tr">` zorunludur: bu nitelik olmadan CSS
`text-transform: uppercase` kuralı `i → I` eşler ve "Sistemi" → "SISTEMI" olur.

## Kaynak dosyalar

Marka kitinin aslı `contact@ytublockchain.com` Drive hesabında
`design/` klasöründedir (logo, font, afiş kaynakları). Bu depoda yalnız deck
üretimi için gereken işlenmiş sürümler tutulur.

## Lisans

Orijinal skill MIT lisanslıdır ([LICENSE](LICENSE)). Marka varlıkları
(logo, fontlar, görseller) YTÜ Blockchain Kulübü'ne aittir ve bu lisansın
kapsamı dışındadır.
