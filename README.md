# YTÜ Blockchain Slides Generator

Kulübün sunum **tasarım sistemi** ve deck üretmek için kullanılan Claude Code
skill'i. Burada deck tutulmaz — üretilen deck'ler
[`slides`](https://github.com/YTU-BLOCKCHAIN/slides) deposunda yaşar ve oradan
yayınlanır.

Bu depo iki şey barındırır:

1. **Tasarım sistemi** — renkler, fontlar, 18 bileşen, kurallar
2. **Skill** — Claude Code'a "nasıl deck üretilir" anlatan talimatlar

## Kurulum

```bash
git clone https://github.com/YTU-BLOCKCHAIN/ytu-blockchain-slides-generator
cd ytu-blockchain-slides-generator
make kur      # fonttools, brotli, Pillow
make          # her şeyi üret
```

Üretilmiş dosyalar depoda tutulmaz; `make` bunları yerelde oluşturur. Sebebi:
içlerinde base64 gömülü font var, commit'lenirlerse her tasarım dokunuşu
kalıcı olarak ~2 MB git geçmişi biriktirir.

Sonra tarayıcıda aç:

```bash
open ytu-brand/components.html    # tasarım sistemi galerisi
open examples/ornek-deck.html     # 8 slaytlık örnek deck
```

## Deck nasıl üretilir

Claude Code'u bu depoda aç ve iste:

> Solidity ders 04 için deck yap, konu reentrancy açığı

Skill sırayla:

1. Amaç, uzunluk, içerik ve yoğunluk sorar — **stil sormaz**, stil sabittir
2. `ytu-brand/design.md`'yi baştan sona okur
3. Slayt planını onaya sunar
4. Tek dosya HTML üretir, tarayıcıda açar
5. Ekran görüntüsüyle taşma ve çakışma kontrol eder

Üretilen deck'i `slides` deposuna taşıyıp PR açarsın.

## Marka kitini güncelleme

`slides` deposu tasarım dosyalarının kopyasını taşır. Tasarımı burada
değiştirdikten sonra:

```bash
make kit      # dist/kit/ altına toplar (~200 KB)
```

Sonra `slides` deposunda `./marka-guncelle` çalıştırılır; kit oradaki `brand/`
klasörüne kopyalanır ve bütün deck'ler yeni tasarımla yeniden üretilir.

Kitin içeriği: `brand.css`, `viewport-base.css`, `deck.js`, `design.md`,
`assets/mark.svg`. Kaynak dosyalar (`brand.src.css`, fontlar, `tools/`) burada
kalır — deck yazan kişinin bunlara erişmesi gerekmiyor.

## Depo yapısı

```
SKILL.md              Skill akışı (Phase 0-6)
html-template.md      HTML iskeleti
animation-patterns.md İzin verilen üç hareket
viewport-base.css     Sabit 16:9 sahne mekaniği

ytu-brand/
  design.md           TASARIM ANAYASASI — deck üretmeden önce okunur
  brand.src.css       Kaynak stil (elle düzenlenir)
  brand.css           ÜRETİLMİŞ — fontlar base64 gömülü
  deck.js             Slayt denetleyicisi
  components.src.html Galeri kaynağı
  components.html     ÜRETİLMİŞ — canlı bileşen galerisi
  fonts/              EAS VHS TR (yamalı) + Clash Grotesk
  assets/             Logo ve dither'lanmış görseller
  tools/
    patch-eas-vhs.py    Fonta Türkçe glifleri ve tabular rakamları ekler
    build-brand-css.py  brand.src.css + fontlar -> brand.css
    build-gallery.py    Galeri
    build-example.py    Örnek deck
    dither.py           Fotoğrafı 1-bit marka görseline çevirir

examples/             Örnek deck (kaynak + üretilmiş)
scripts/              PPTX çıkarma, PDF aktarımı, Vercel dağıtımı
```

**Kural:** adında `.src.` olan dosya elle düzenlenir, olmayan üretilir.
Üretilmiş bir dosyayı elle düzenlersen bir sonraki `make`'te kaybolur.

## Tasarım sistemi özeti

| | |
|---|---|
| Yüzeyler | `#0A0A0C` void · `#0E6CFF` signal · `#000560` deep |
| Fontlar | EAS VHS TR (display) · Clash Grotesk (gövde) |
| Izgara | 24px blok — logonun 12.494 birimlik modülünden türetildi |
| Sahne | 1920×1080 sabit, tek transform ile ölçeklenir |
| İmza öğeleri | Film grain · 1-bit dither görsel · köşeli etiket · mavi vurgu bandı |

Gerekçeleriyle birlikte tamamı: [`ytu-brand/design.md`](ytu-brand/design.md)

## Bilinmesi gereken iki tuzak

**Türkçe büyük harf.** Deck'lerde `<html lang="tr">` zorunlu. Yoksa CSS
`text-transform: uppercase` kuralı `i → I` eşler ve "Sistemi" → "SISTEMI"
olur. Ama marka adları ve İngilizce terimler (`BLOCKCHAIN`, `BITCOIN`,
`SATOSHI`) HTML'e **elle büyük harf** yazılır — aksi hâlde aynı kural onlara
da Türkçe uygular ve logodaki noktasız I bozulur.

**Font yaması.** `fonts/eas-vhs-tr.woff2` orijinal değil. EAS VHS'te Ğ, İ, Ş,
ğ, ş glifleri yoktu (eski afişlerde "BAŞVURU" yerine "BASVURU" yazmasının
sebebi bu) ve rakamlar üç farklı genişlikteydi. `make font` yamayı Drive'daki
orijinalden yeniden üretir.

## Görseller

Deck'e giren her fotoğraf 1-bit dither'dan geçer:

```bash
python3 ytu-brand/tools/dither.py girdi.jpg cikti.png --width 900
```

Çıktı beyaz nokta matrisi + şeffaf zemindir; aynı dosya hem koyu hem mavi
yüzeyde çalışır. Portre için `--width 700`, geniş görsel için `--width 1200`.

İşlenmemiş fotoğraf kullanılmaz — sistemin dışında durur ve slaytı yamalı
gösterir.

## Kaynak dosyalar

Marka kitinin aslı (logo, font, afiş kaynakları) `contact@ytublockchain.com`
Drive hesabında `design/` klasöründedir. Bu depoda yalnız deck üretimi için
gereken işlenmiş sürümler tutulur.

## Lisans

Orijinal skill [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)
forkudur, MIT lisanslıdır ([LICENSE](LICENSE)). Marka varlıkları (logo,
fontlar, görseller) YTÜ Blockchain Kulübü'ne aittir ve bu lisansın kapsamı
dışındadır.
