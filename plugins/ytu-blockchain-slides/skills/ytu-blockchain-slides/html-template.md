# HTML Sunum İskeleti

Deck üretiminin referans mimarisi. Her sunum sabit 16:9 sahne modelini izler:
slaytlar 1920×1080'de yazılır, sahnenin tamamı tarayıcı penceresine ölçeklenir.

Renk, punto ve bileşen tanımları burada **yoktur** — hepsi `ytu-brand/brand.css`
içinde. Bu dosya yalnız iskeleti ve davranışı anlatır.

## Temel HTML Yapısı

```html
<!DOCTYPE html>
<!-- lang="tr" ZORUNLU: CSS text-transform:uppercase kuralı Türkçe için
     i -> İ eşlemesini ancak bu nitelikle yapar. Yoksa her başlıkta
     "SISTEMI", "ETKINLIK" gibi bozuk çıktı oluşur. -->
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sunum Başlığı</title>

    <!-- Harici font linki YOK. Fontlar brand.css içinde base64 gömülü;
         sunum sırasında ağ bağlantısı garanti değil. -->

    <style>
        /* --- ytu-brand/brand.css DOSYASININ TAM İÇERİĞİNİ BURAYA YAPIŞTIR ---
           Tokenlar (--void, --signal, --deep, --b, tip ölçeği), tüm bileşen
           sınıfları ve gömülü fontlar bu dosyadan gelir. Değerleri burada
           yeniden tanımlama. */

        * { margin: 0; padding: 0; box-sizing: border-box; }

        /* --- viewport-base.css İÇERİĞİNİ BURAYA YAPIŞTIR --- */

        /* ===========================================
           ANIMATIONS
           Trigger via .visible class on the active slide
           =========================================== */
        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity var(--duration-normal) var(--ease-out-expo),
                        transform var(--duration-normal) var(--ease-out-expo);
        }

        .slide.visible .reveal {
            opacity: 1;
            transform: translateY(0);
        }

        /* Stagger children for sequential reveal */
        .reveal:nth-child(1) { transition-delay: 0.1s; }
        .reveal:nth-child(2) { transition-delay: 0.2s; }
        .reveal:nth-child(3) { transition-delay: 0.3s; }
        .reveal:nth-child(4) { transition-delay: 0.4s; }

    </style>
</head>
<body>
    <div class="deck-viewport">
        <main class="deck-stage" id="deckStage">
            <!-- Kapak arketipi. Marka adı elle büyük harf yazılır ki
                 text-transform Türkçe kuralını uygulayıp BLOCKCHAİN yapmasın. -->
            <section class="slide stage active" lang="tr">
                <img class="mark" src="data:image/svg+xml;base64,..." alt="">
                <div class="chrome meta">2026 · BAHAR DÖNEMİ</div>
                <h1 class="d-hero reveal">BLOCKCHAIN<br>101</h1>
                <div class="chrome page"><b>01</b> <span>/ 24</span></div>
            </section>

            <section class="slide">
                <div class="slide-content">
                    <h2 class="reveal">Slide Title</h2>
                    <p class="reveal">Content...</p>
                </div>
            </section>

            <!-- More slides... -->
        </main>
    </div>

    <script>
        /* ===========================================
           SLIDE PRESENTATION CONTROLLER
           =========================================== */
        class SlidePresentation {
            constructor() {
                this.slides = document.querySelectorAll('.slide');
                this.currentSlide = 0;
                this.stage = document.getElementById('deckStage');
                this.setupStageScale();
                this.setupKeyboardNav();
                this.setupTouchNav();
                this.showSlide(0);
            }

            setupStageScale() {
                const scale = () => {
                    const factor = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
                    const x = (window.innerWidth - 1920 * factor) / 2;
                    const y = (window.innerHeight - 1080 * factor) / 2;
                    this.stage.style.transform = `translate(${x}px, ${y}px) scale(${factor})`;
                };
                scale();
                window.addEventListener('resize', scale);
            }

            setupKeyboardNav() {
                // Arrow keys, Space, Page Up/Down
            }

            setupTouchNav() {
                // Touch/swipe support for mobile
            }

            showSlide(index) {
                this.currentSlide = Math.max(0, Math.min(index, this.slides.length - 1));
                this.slides.forEach((slide, i) => {
                    slide.classList.toggle('active', i === this.currentSlide);
                    slide.classList.toggle('visible', i === this.currentSlide);
                });
            }
        }

        new SlidePresentation();
    </script>
</body>
</html>
```

## Required JavaScript Features

Every presentation must include:

1. **SlidePresentation Class** — Main controller with:
   - Keyboard navigation (arrows, space, page up/down)
   - Touch/swipe support
   - Mouse wheel navigation
   - Optional progress indicator or page count, kept outside the slide stage

2. **Sahne Ölçekleme** — Sabit 16:9 davranışı için:
   - Bütün slaytlar `.deck-stage` içinde 1920×1080 kalır
   - Sahne tek bir transform ile ölçeklenir
   - Letterbox/pillarbox olabilir; içerik cihaza göre yeniden akmaz
   - **Letterbox rengi aktif slaytın yüzeyine eşitlenir.** Sabit koyu
     bırakılırsa mavi slayt ekranın ortasında bir dikdörtgen gibi görünür:

   ```js
   function surfaceOf(slide) {
     if (slide.classList.contains('stage--signal')) return 'var(--signal)';
     if (slide.classList.contains('stage--deep')) return 'var(--deep)';
     return 'var(--void)';
   }
   // slayt her degistiginde:
   var surface = surfaceOf(slides[index]);
   document.documentElement.style.setProperty('--stage-bg', surface);
   document.documentElement.style.setProperty('--slide-bg', surface);
   ```

3. **İlerleme Çubuğu** — `.prog` segmentlerini data niteliklerinden kurar:

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

   Ek süsleme eklenmez: parçacık arka planı, özel imleç, parallax, 3B eğilme
   ve manyetik düğme bu sistemin dili değildir. Hareket yalnız slayt geçişi
   ve `.reveal` kademeli girişiyle sınırlıdır.

4. **Inline Editing** (included by default after draft generation):
   - Edit toggle button (hidden by default, revealed via hover hotzone or `E` key)
   - Auto-save to localStorage
   - Export/save file functionality
   - See "Inline Editing Implementation" section below

## Inline Editing Implementation

Inline editing is a lightweight post-draft affordance. Do not ask the user whether they want it during the pre-generation Q&A. Include it by default unless the user explicitly asks for a locked/export-only presentation or no editing controls.

**Do NOT use CSS `~` sibling selector for hover-based show/hide.** The CSS-only approach (`edit-hotzone:hover ~ .edit-toggle`) fails because `pointer-events: none` on the toggle button breaks the hover chain: user hovers hotzone -> button becomes visible -> mouse moves toward button -> leaves hotzone -> button disappears before click.

**Required approach: JS-based hover with 400ms delay timeout.**

HTML:
```html
<div class="edit-hotzone"></div>
<button class="edit-toggle" id="editToggle" title="Edit mode (E)">✏️</button>
```

CSS (visibility controlled by JS classes only):
```css
/* Do NOT use CSS ~ sibling selector for this!
   pointer-events: none breaks the hover chain.
   Must use JS with delay timeout. */
.edit-hotzone {
    position: fixed; top: 0; left: 0;
    width: 80px; height: 80px;
    z-index: 10000;
    cursor: pointer;
}
.edit-toggle {
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
    z-index: 10001;
}
.edit-toggle.show,
.edit-toggle.active {
    opacity: 1;
    pointer-events: auto;
}
```

JS (three interaction methods):
```javascript
// 1. Click handler on the toggle button
document.getElementById('editToggle').addEventListener('click', () => {
    editor.toggleEditMode();
});

// 2. Hotzone hover with 400ms grace period
const hotzone = document.querySelector('.edit-hotzone');
const editToggle = document.getElementById('editToggle');
let hideTimeout = null;

hotzone.addEventListener('mouseenter', () => {
    clearTimeout(hideTimeout);
    editToggle.classList.add('show');
});
hotzone.addEventListener('mouseleave', () => {
    hideTimeout = setTimeout(() => {
        if (!editor.isActive) editToggle.classList.remove('show');
    }, 400);
});
editToggle.addEventListener('mouseenter', () => {
    clearTimeout(hideTimeout);
});
editToggle.addEventListener('mouseleave', () => {
    hideTimeout = setTimeout(() => {
        if (!editor.isActive) editToggle.classList.remove('show');
    }, 400);
});

// 3. Hotzone direct click
hotzone.addEventListener('click', () => {
    editor.toggleEditMode();
});

// 4. Keyboard shortcut (E key, skip when editing text)
document.addEventListener('keydown', (e) => {
    if ((e.key === 'e' || e.key === 'E') && !e.target.getAttribute('contenteditable')) {
        editor.toggleEditMode();
    }
});
```

## Görsel Boru Hattı (Görsel Yoksa Atla)

Deck'e giren **her** fotoğraf 1-bit dither'dan geçer. İşlenmemiş fotoğraf
sistemin dışında durur ve slaytı yamalı gösterir.

**Bağımlılık:** `pip install Pillow`

```bash
# portre / dikey görsel
python ytu-brand/tools/dither.py girdi.jpg cikti.png --width 700

# geniş görsel, harita, diyagram
python ytu-brand/tools/dither.py girdi.jpg cikti.png --width 1200
```

Çıktı beyaz nokta matrisi + şeffaf zemindir; aynı dosya hem `--void` hem
`--signal` yüzeyinde çalışır. `--width` nokta yoğunluğunu belirler: küçük değer
iri nokta, büyük değer ince nokta.

İşlenen dosya base64 olarak deck'e gömülür ve `class="dither"` ile yerleştirilir.

| Durum | İşlem |
|-------|-------|
| Konuşmacı portresi | `--width 700` |
| Geniş görsel / harita | `--width 1200` |
| Çok karanlık fotoğraf | `--contrast 1.6` ile tekrar dene |
| Kulüp logosu | İşleme yok — `ytu-brand/assets/mark.svg` kullan |

CSS filtresiyle taklit etme. Gerçek Floyd–Steinberg dither ile CSS nokta maskesi
aynı şey değildir; ikincisi ucuz durur.

### Image Placement

**Use direct file paths** (not base64) — presentations are viewed locally:

```html
<img src="assets/logo_round.png" alt="Logo" class="slide-image logo">
<img src="assets/screenshot.png" alt="Screenshot" class="slide-image screenshot">
```

```css
.slide-image {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
    border-radius: 8px;
}
.slide-image.screenshot {
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.slide-image.logo {
    max-height: min(30vh, 200px);
}
```

**Adapt border/shadow colors to match the chosen style's accent.** Never repeat the same image on multiple slides (except logos on title + closing).

**Placement patterns:** Logo centered on title slide. Screenshots in two-column layouts with text. Full-bleed images as slide backgrounds with text overlay (use sparingly).

---

## Code Quality

**Comments:** Every section needs clear comments explaining what it does and how to modify it.

**Accessibility:**
- Semantic HTML (`<section>`, `<nav>`, `<main>`)
- Keyboard navigation works fully
- ARIA labels where needed
- `prefers-reduced-motion` support (included in viewport-base.css)

## File Structure

Single presentations:
```
presentation.html    # Self-contained, all CSS/JS inline
assets/              # Images only, if any
```

Multiple presentations in one project:
```
[name].html
[name]-assets/
```
