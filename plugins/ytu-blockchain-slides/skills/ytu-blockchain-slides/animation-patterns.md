# Hareket

Bu sistemde hareket bir stil tercihi değil, **sabit bir davranış**. Deck'ten
deck'e değişmez; "bu sunuma özel bir geçiş" eklenmez.

Toplam repertuvar üç şeyden ibaret: slayt geçişi, içerik girişi, ilerleme
çubuğu. Başka hareket yok.

## 1. Slayt geçişi

Görünürlük `.active` / `.visible` sınıflarıyla yönetilir, **`display` ile
değil**. Sebep: sonradan gelen bir layout kuralı (`.slide-content { display:
flex }` gibi) `display:none`'ı ezip bütün slaytları aynı anda görünür yapabilir.
`viewport-base.css` bunu `visibility`, `opacity` ve `pointer-events` üzerinden
çözer.

```css
.slide {
  visibility: hidden;
  opacity: 0;
  pointer-events: none;
}
.slide.active,
.slide.visible {
  visibility: visible;
  opacity: 1;
  pointer-events: auto;
}
```

Geçiş süresi eklenmez; slayt anında değişir. Sunum sırasında bekleme hissi
yaratmaz.

## 2. İçerik girişi

Slayt görünür olunca içerik aşağıdan kademeli belirir. Tek easing, tek süre.

```css
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide.visible .reveal { opacity: 1; transform: none; }

.slide.visible .reveal:nth-child(1) { transition-delay: 0.05s; }
.slide.visible .reveal:nth-child(2) { transition-delay: 0.12s; }
.slide.visible .reveal:nth-child(3) { transition-delay: 0.19s; }
.slide.visible .reveal:nth-child(4) { transition-delay: 0.26s; }
```

Bir slaytta en fazla **dört** `.reveal` öğesi olur. Daha fazlası kademeyi
sürükler ve sunucu konuşmaya başlamadan animasyon bitmemiş olur.

Kademe sırası okuma sırasıdır: etiket → başlık → ayraç → gövde.

## 3. İlerleme çubuğu

Animasyon değil, durum göstergesi. Slayt yüklendiğinde JavaScript ile kurulur;
geçişte yeniden çizilir, hareket etmez.

```js
document.querySelectorAll('.prog').forEach(function (bar) {
  var total = Number(bar.dataset.total) || 0;
  var now = Number(bar.dataset.now) || 0;
  var out = '';
  for (var i = 1; i <= total; i++) {
    out += '<i class="' + (i < now ? 'on' : i === now ? 'now' : '') + '"></i>';
  }
  bar.innerHTML = out;
});
```

## Kullanılmayanlar

Aşağıdakiler bu sistemin dili değildir ve eklenmez:

- Parçacık sistemi, canvas arka planı
- Neon parlama, glow, box-shadow efekti
- Glitch / karakter karıştırma animasyonu
- Parallax, 3B eğilme, manyetik düğme
- Özel imleç, imleç izi
- Sayaç animasyonu (istatistik rakamları sabit durur)
- Slaytlar arası kayma, çevirme, zoom geçişi

Gerekçe: sistem düz ve köşeli. Derinlik ve hareket yerine tipografi, blok
ızgarası ve dither dokusu çalışır. Efekt eklemek deck'i "sunum şablonu"
görüntüsüne düşürür.

## Azaltılmış hareket

`prefers-reduced-motion` desteği `viewport-base.css` ve `brand.css` içinde
zaten tanımlı. Ek bir şey yapılmaz; yeni bir `transition` yazarsan bu blokların
kapsamına girdiğinden emin ol.
