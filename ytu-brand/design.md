---
name: YTÜ Blockchain
version: 1
description: >
  YTÜ Blockchain Kulübü'nün tek deck tasarım sistemi. Koyu zemin, film grain,
  1-bit dither görseller ve köşeli etiketler üzerine kurulu; marka kitindeki
  afiş ve banner dilinin sunum yüzeyine taşınmış hâli. Bu depoda başka stil
  yoktur — her deck bu sistemden çıkar.

colors:
  void: "#0A0A0C"
  signal: "#0E6CFF"
  deep: "#000560"
  ink: "#FFFFFF"

fonts:
  display: "EAS VHS TR"
  body: "Clash Grotesk"

stage: 1920x1080
block: 24px
---

# YTÜ Blockchain Deck Sistemi

## Bu dosya nasıl kullanılır

Deck üretirken sırayla:

1. Bu dosyayı **tamamen** oku. Stil seçeneği yoktur; seçilecek bir şey yok.
2. `brand.css` dosyasının **tam içeriğini** deck'in `<style>` bloğuna kopyala.
   Fontlar bu dosyanın içinde base64 gömülü — harici istek yapma.
3. `viewport-base.css` içeriğini de ekle.
4. `html-template.md`'deki iskeleti kullan.
5. Slaytları aşağıdaki **arketiplerden** kur. Yeni arketip icat etme.
6. Üretilen deck'i tarayıcıda aç, ekran görüntüsü al, taşma ve çakışma kontrol
   et. `scrollHeight` kontrolü tek başına yetmez — bir panel diğerinin üstünü
   örtebilir ve bu yalnız görselde fark edilir.

Canlı referans: `components.html`. Bir bileşenin nasıl görünmesi gerektiğinden
emin değilsen önce oraya bak.

## Sabit sahne

Her deck **1920×1080 sabit sahne**dir ve tarayıcı penceresine tek bir
`transform: scale()` ile ölçeklenir. Telefonda bile 16:9 korunur; letterbox
olabilir, ama içerik asla yeniden akmaz.

Bu yüzden ölçülerde `vw`, `vh`, `clamp()` kullanılmaz — hepsi sabit `px`.

### Letterbox rengi

Ekran oranı 16:9 tutmadığında yanlarda (ya da altta/üstte) boşluk kalır. Bu
boşluk **aktif slaytın yüzey rengine eşitlenir**; sabit koyu bırakılırsa mavi
bir slayt ekranın ortasında duran bir dikdörtgen gibi görünür ve deck "tam
ekran değil" hissi verir.

Deck denetleyicisi slayt değiştikçe `--stage-bg` ve `--slide-bg` değişkenlerini
günceller. Örnek uygulama: `examples/ornek-deck.html`.

> CSS'te `transform: scale(calc(100cqw / 1920))` **yazma**. Uzunluğu sayıya
> bölmek yine uzunluk verir, `scale()` sayı bekler, kural sessizce yok sayılır
> ve sahne 1:1 render edilip kırpılır. Ölçek JavaScript ile hesaplanır.

## Yüzeyler

Üç yüzey var, her birinin işi ayrı. Bir slayt yalnız birini kullanır; aynı
slaytta iki yüzey karışmaz.

| Token | Değer | Sınıf | Nerede |
|---|---|---|---|
| Void | `#0A0A0C` | `.stage` | İçerik slaytlarının tamamı. Varsayılan. |
| Signal | `#0E6CFF` | `.stage--signal` | Bölüm ayracı, istatistik, kapanış. |
| Deep | `#000560` | `.stage--deep` | Logo kilidi, derin ikincil blok. Seyrek. |

Void nötr siyah değil, hafif mavi yanlı — marka mavisiyle aynı ailede okunsun
diye. Değiştirme.

**Signal kullanım oranı:** 24 slaytlık bir deck'te en fazla 4–5 mavi slayt.
Daha fazlası vurguyu öldürür; mavi ancak nadir olduğu sürece "dikkat" demektir.

### Mürekkep

Tek mürekkep rengi vardır: **beyaz**. Hiyerarşi gri tonlarıyla değil,
saydamlıkla kurulur (`--ink-dim`, `--ink-faint`, `--rule`). Böylece aynı
kademeler üç yüzeyde de çalışır.

Palette kırmızı, yeşil, sarı **yoktur**. Uyarı kutusunda bile. Vurgu gerekiyorsa
punto büyütülür, etiket eklenir ya da marka mavisi kullanılır.

## Tipografi

İki font. Üçüncüsü eklenmez.

- **EAS VHS TR** — display ve chrome. Her zaman büyük harf.
- **Clash Grotesk** — gövde metni. Küçük harf yalnız burada kullanılır.

### Türkçe büyük harf kuralı

Bu sistemin en kolay bozulan yeri. İki ayrı kural var:

**1. `lang="tr"` zorunlu.** `<html lang="tr">` yoksa CSS `text-transform:
uppercase` kuralı `i → I` eşler; Türkçede doğrusu `i → İ`'dir. Bu olmadan
"Sistemi" → "SISTEMI", "Etkinlik" → "ETKINLIK" olur ve her başlık sessizce
bozulur.

**2. Marka adları ve İngilizce terimler doğrudan büyük harf yazılır.**
`lang="tr"` açıkken dönüşüm bu kelimelere de Türkçe kuralını uygular ve
"Blockchain" → "BLOCKCHAİN" olur — oysa kulübün logosunda **noktasız I**
vardır.

```html
<!-- doğru -->
<h1 class="d-hero">BLOCKCHAIN<br>101</h1>     <!-- marka: elle büyük harf -->
<h3 class="d-headline">Zincir Karşılaştırması</h3>  <!-- Türkçe: dönüşüme bırak -->

<!-- yanlış -->
<h1 class="d-hero">Blockchain<br>101</h1>     <!-- BLOCKCHAİN olur -->
```

Elle büyük harf yazılacaklar: `BLOCKCHAIN`, `BITCOIN`, `SOLIDITY`, `SATOSHI`,
URL'ler, kullanıcı adları, tüm özel adlar ve İngilizce terimler.

### Font notu

`fonts/eas-vhs-tr.woff2` yamalanmış bir dosyadır. Orijinal EAS VHS'te **Ğ, İ,
Ş, ğ, ş glifleri yoktu** — marka kitindeki eski afişlerde "BAŞVURU" yerine
"BASVURU" yazmasının sebebi budur. Ayrıca rakamlar farklı genişlikteydi, bu da
sayfa sayacında ve tablo sütunlarında kaymaya yol açıyordu.

`tools/patch-eas-vhs.py` bu beş glifi fontun kendi yarım-piksel ızgarasına
(120.5 birim) oturacak şekilde üretir ve rakamları tabular hâle getirir. Font
güncellenirse betik yeniden çalıştırılmalı, ardından `tools/build-brand-css.py`.

### Ölçek

Sahne 1920×1080 olduğu için hepsi sabit px.

| Sınıf | Punto | Satır | Kullanım |
|---|---|---|---|
| `.d-hero` | 176 | 1.10 | Yalnız kapak. Deck'te bir kez. |
| `.d-title` | 128 | 1.10 | Kapanış. |
| `.d-chapter` | 104 | 1.12 | Bölüm ayracı. |
| `.d-headline` | 68 | 1.14 | İçerik slaytı başlığı. |
| `.d-subhead` | 42 | 1.18 | Slayt içi alt başlık. |
| `.lead` | 34 | 1.35 | Giriş cümlesi. En fazla 24 karakter genişlik. |
| `.body` | 26 | 1.50 | Gövde. En fazla 34 karakter genişlik. |
| `.small` | 20 | 1.45 | İkincil metin, tablo hücresi. |
| `.chrome` | 18 | 1.00 | Sayfa numarası, etiket, üst bilgi. |

Ara punto uydurma. Bir metin sığmıyorsa punto düşürülmez — **metin kısaltılır
ya da slayt bölünür**.

### Satır yüksekliği neden bu kadar açık

Display satır yükseklikleri Türkçeye göre belirlendi, estetiğe göre değil.
Fontun dikey sınırları (em): büyük harf tepesi 0.823, İ noktası ve Ğ breve
tepesi 1.000, Ş/Ç sedilla dibi −0.235.

Daha sıkı değerlerde bir satırın sedillası alttaki satırın harfine giriyor:
"BAŞLANGIÇ / GÜVENLİĞİ" 1.06'da çakışıyor, 1.10'da temizleniyor. Değerler
ölçülerek bulundu — teorik en kötü durum 1.235 isterdi ama gerçek metinde
sedilla ile aksan aynı x konumuna nadiren denk gelir.

**Bu değerleri düşürme.** Bir başlık fazla açık duruyorsa satırı yeniden böl,
satır yüksekliğini kısma.

Kenar durum: bir satır Ç/Ş ile bitip alttaki satırda tam o hizada Ğ/İ/Ü varsa
yine değebilir. Çözümü yine satırı yeniden bölmektir.

## Izgara

Logonun harfleri 12.494 birimlik bir modül üzerine çizilmiş; tüm koordinatları
bu sayının katı. 1920×1080 sahnede karşılığı **24px**.

```
--b       24px    blok birimi (logonun modülü)
--u        8px    alt birim (b/3)
--margin  96px    kenar boşluğu (4b)
--gutter  24px    sütun aralığı (b)
--col       12    sütun sayısı
```

Grafik bar yükseklikleri, ilerleme segmentleri, tablo satır yükseklikleri ve
boşluklar bu modülün katıdır. Bileşenlerin aynı aileden görünmesinin sebebi
budur — bozma.

## Slayt arketipleri

Her deck bu beşin tekrarıdır.

### 1. Kapak
Void. Sol alta hizalı blok: `.tag` → `.d-hero` → `.rule-block` → `.lead`.
Sunan bilgisi sol altta `.chrome`, sayfa numarası sağ altta. İlerleme çubuğu
**yok** (deck henüz başlamadı).

### 2. Bölüm ayracı
Signal. Solda dikey ortalanmış: büyük bölüm numarası (opaklık .42) →
`.d-chapter` → `.lead`. Sağ yarı bilerek boş bırakılır.

### 3. İçerik
Void. `.body-area` içinde iki sütun: solda `.tag` + `.d-headline` + `.body`,
sağda dither görsel ya da bileşen. Slayt başına **en fazla bir** `.hl` vurgu
bandı.

### 4. Veri
Void. `.d-headline` + tablo / grafik / diyagram. Yoğun slayt; boşluk bırakmak
yerine doldurulur.

### 5. Kapanış
Signal. `.d-title` + `.lead` + iletişim `.tag`'leri. Sayfa göstergesi kalır,
ilerleme çubuğu kalkar — deck bitti sinyali.

## Slayt chrome'u

Her slaytta aynı dört öğe, aynı yerde. Biri eksikse deck dağılmış görünür.

```html
<img class="mark" src="…mark.svg" alt="">           <!-- sol üst, 56px -->
<div class="chrome meta">BÖLÜM · ALT BAŞLIK</div>   <!-- sağ üst -->
<div class="prog" data-total="24" data-now="8"></div><!-- sol alt -->
<div class="chrome page"><b>08</b> <span>/ 24</span></div>  <!-- sağ alt -->
```

`.prog` segmentleri JavaScript ile kurulur; `data-total` slayt sayısı,
`data-now` bulunulan slayt.

## Bileşen grameri

Tam ve çalışan örnekleri için `components.html`.

### Ortak
| Sınıf | Ne |
|---|---|
| `.tag` | Köşeli etiket kutusu. `--signal` `--solid` `--quiet` varyantları. |
| `.hl` | Metin arkasında dolu mavi vurgu bandı. Slayt başına bir kez. |
| `.rule-block` | Merdiven basamaklı ayraç. Düz çizgi yerine bunu kullan. |
| `.tbl` | Tablo. `.num` sağa dayalı ve tabular, `tr.hi` vurgulu satır. |
| `.stat` | Dev rakam + etiket. Signal yüzeyinde en güçlü. |

### Eğitim
| Sınıf | Ne |
|---|---|
| `.code` | Kod bloğu. Renklendirme üç tonla sınırlı: `.k` anahtar, `.c` yorum, `.s` değer. `.hi` vurgulu satır. |
| `.term` | Terim/tanım kutusu. `<dl><dt><dd>`. |
| `.note` | Not kutusu. `--info` `--warn` `--danger`. |
| `.steps` | Numaralı adım akışı. **Yalnız gerçekten sıralı içerikte.** |
| `.compare` | İki sütun karşılaştırma. |

### Etkinlik
| Sınıf | Ne |
|---|---|
| `.speaker` | Konuşmacı kartı. Portre dither'dan geçmiş olmalı. |
| `.agenda` | Saat / başlık / yer satırları. |
| `.sponsors` | Sponsor ızgarası. Kademe **boyutla** belirtilir; `.lead` iki hücre kaplar. "Altın/gümüş" etiketi kullanılmaz. |
| `.timeline` | Yatay zaman çizelgesi, `.on` geçmiş kilometre taşı. |

### Veri
| Sınıf | Ne |
|---|---|
| `.bars` | Bar grafik. Yükseklikler 24'ün katına yuvarlanır. Aynı anda **tek** bar vurgulanır, gerisi `.mute`. |
| `.chain` | Blok zinciri diyagramı. `.on` aktif blok. |

## Görsel işleme

**Deck'e giren her fotoğraf dither'dan geçer.** İşlenmemiş fotoğraf sistemin
dışında durur ve slaytı yamalı gösterir.

```bash
python tools/dither.py girdi.jpg cikti.png --width 900
```

Çıktı beyaz nokta matrisi + şeffaf zemindir; aynı dosya hem void hem signal
üzerinde çalışır. `--width` nokta yoğunluğunu belirler: portre için 700,
geniş görsel için 1200 civarı.

CSS filtresiyle taklit etme — gerçek Floyd–Steinberg dither ile CSS'in nokta
maskesi aynı şey değil, ikincisi ucuz durur.

## Yapılır

- Metni kısalt, puntoyu koru.
- Bir slaytta tek vurgu: ya `.hl`, ya vurgulu tablo satırı, ya mavi bar.
- Türkçe metni `text-transform`'a bırak, marka adlarını elle büyük harf yaz.
- Sayfa numarasını ve logoyu her slaytta koru.
- Üretimden sonra tarayıcıda görsel doğrulama yap.

## Yapılmaz

- Yeni renk eklemek. Palet üç yüzey + beyaz, o kadar.
- Üçüncü font eklemek.
- Gradient, gölge, yuvarlatılmış köşe. Sistem düz ve köşeli.
- Emoji. Hiçbir yerde.
- Aynı slaytta iki mavi vurgu.
- İşlenmemiş fotoğraf koymak.
- `.steps` numaralandırmasını sırasız listede kullanmak.
- Punto ölçeğinin dışına çıkmak.
