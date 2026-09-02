---
name: ytu-blockchain-slides
description: YTÜ Blockchain Kulübü için HTML sunum üretir. Ders anlatımı, etkinlik duyurusu, sponsor sunumu, hackathon deck'i ya da PPTX dönüşümü istendiğinde kullanılır. Tek ve kilitli bir marka tasarım sistemi vardır — stil seçimi sunulmaz, her deck aynı görünür.
---

# YTÜ Blockchain Slides

Kulübün tüm sunumlarını tek bir marka tasarım sisteminden üretir. Bağımlılıksız, tek dosya HTML; fontlar ve görseller gömülü, ağ bağlantısı gerekmez.

**Tasarım sistemi kilitlidir.** `ytu-brand/design.md` tek kaynaktır; stil seçeneği üretilmez, kullanıcıya sorulmaz.

## Core Principles

1. **Bağımlılık yok** — Tek HTML dosyası, CSS/JS satır içi. Fontlar base64 gömülü.
2. **Tek sistem** — Stil seçimi yoktur. Her deck `ytu-brand/design.md` sisteminden çıkar; kullanıcıya stil seçeneği sunulmaz, alternatif tema üretilmez.
3. **Tutarlılık > yaratıcılık** — Bu deponun amacı her sunumun aynı görünmesi. "Bu deck'e özel" bir dokunuş eklemek sistemi bozar.
4. **Türkçe doğru dizilir** — `<html lang="tr">` zorunlu; marka adları ve İngilizce terimler elle büyük harf yazılır. Ayrıntı: `ytu-brand/design.md`.
5. **Sabit 16:9 sahne (PAZARLIKSIZ)** — Her deck 1920×1080 sahnedir ve viewport'a bir bütün olarak ölçeklenir. Telefonda dahi 16:9 korunur; içerik yeniden akmaz.

## Tasarım Sistemi

Bu depoda tasarım kararı verilmez; sistem hazırdır ve `ytu-brand/` altındadır.

| Dosya | Ne işe yarar |
| --- | --- |
| `ytu-brand/design.md` | Sistemin anayasası. Üretimden önce **tamamen** okunur. |
| `ytu-brand/brand.css` | Tokenlar, bileşenler ve base64 gömülü fontlar. **Tam içeriği** deck'e kopyalanır. |
| `ytu-brand/components.html` | Canlı bileşen galerisi. Bir bileşenin görünümünden emin değilsen buraya bak. |
| `ytu-brand/assets/` | Logo ve dither'lanmış görseller. |
| `ytu-brand/tools/dither.py` | Deck'e girecek her fotoğrafı marka diline çevirir. |

Özet: koyu `#0A0A0C` zemin, marka mavisi `#0E6CFF` vurgu, `#000560` lacivert;
EAS VHS TR (display) + Clash Grotesk (gövde); film grain; 1-bit dither
görseller; köşeli etiketler; 24px blok ızgarası.

**Yapılmayacaklar:** yeni renk, üçüncü font, gradient, gölge, yuvarlatılmış
köşe, emoji, işlenmemiş fotoğraf. Gerekçesi `design.md`'de.

## Fixed Stage Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every deck has a viewport wrapper that fills the browser window.
- Every slide is authored inside a fixed 1920×1080 stage.
- The stage scales uniformly to fit the viewport. It may letterbox/pillarbox; it must not re-layout content.
- Do not use responsive breakpoints to rearrange slide content for phones.
- Use fixed internal slide measurements at the 1920×1080 design size.
- Slide visibility must be controlled by `.active` / `.visible` using `visibility`, `opacity`, and `pointer-events` from `viewport-base.css`. Do not use `display: none` / `display: block` for slide switching; later layout classes such as `.slide-content { display: flex; }` can override them and make every slide visible at once.
- Use `clamp()` only for non-slide UI outside the stage, or for small fallback previews where a full stage is impractical.
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Modes

Ask the user whether this is primarily a reading deck or a speaking deck, then design around that answer:

| Density mode | Best for | Design behavior |
| ------------- | -------- | --------------- |
| **Low density / speaker-led** | Public talks, keynote-style sharing, live explanation | One idea per slide, large type, strong visual hierarchy, generous negative space, 1-3 bullets max, more slides if needed |
| **High density / reading-first** | Reports, handouts, async review, detailed internal docs | More self-contained slides, structured grids/tables/annotations, 4-8 bullets or 4-6 cards when readable, tighter but still intentional spacing |

Baseline limits still apply: no scrolling, no overflow, no overlapping panels, and no text below comfortable reading size. If content exceeds the selected density mode, split it into more slides instead of shrinking until it becomes cramped.

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**

### Mode C: Modification Rules

When enhancing existing presentations, fixed-stage fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Fit them inside the 1920×1080 slide canvas. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** the slide stage remains 16:9, no text overflows its card, no panels overlap, and screenshots look correct at 1280×720 plus one phone viewport
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to a new slide or reduce other content first. Never add images without checking if existing content already fills the 1920×1080 slide stage.

---

## Phase 1: Content Discovery (New Presentations)

**Ask ALL questions together** so the user fills everything out at once. If the current environment provides a native structured-question UI, use it; otherwise ask in one concise message with clearly numbered choices:

**Soru 1 — Amaç** (başlık: "Amaç"):
Bu sunum ne için? Seçenekler: Ders/eğitim / Etkinlik duyurusu / Sponsor sunumu / Hackathon veya demo / Kulüp içi

**Soru 2 — Uzunluk** (başlık: "Uzunluk"):
Yaklaşık kaç slayt? Seçenekler: Kısa 5-10 / Orta 10-20 / Uzun 20+

**Soru 3 — İçerik** (başlık: "İçerik"):
İçerik hazır mı? Seçenekler: Tamamı hazır / Kaba notlar / Sadece konu başlığı

**Soru 4 — Yoğunluk** (başlık: "Yoğunluk"):
Deck ne kadar dolu olsun? Seçenekler:

- "Düşük / sunucu anlatır" — Büyük fikirler, az kelime, geniş nefes alanı
- "Yüksek / okunmak için" — Kendi kendine yeten slaytlar, tablo ve detay

**Stil sorma.** Stil sabittir; sorulacak bir tasarım kararı yoktur.

**Do not ask about inline editing during Phase 1.** Users should not have to choose editing behavior before seeing a draft. Inline editing is a post-draft affordance: include it by default unless the user explicitly asks for a locked/export-only file.

Remember the user's density choice. It affects slide count, typography scale, amount of text per slide, layout density, and whether to favor cinematic presenter slides or self-contained reading slides.

If user has content, ask them to share it.

### Step 1.2: Image Evaluation (if images provided)

Kullanıcı görsel vermediyse Phase 2'ye geç.

If user provides an image folder:

1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **Inspect each image** — Use the agent's available image-understanding capability. If image reading is unavailable, use filenames/metadata and ask the user to clarify only when needed
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm the outline** using the same structured-question mechanism when available: "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

**Görseller dither'dan geçer.** Kullanılabilir bulunan her fotoğraf `python ytu-brand/tools/dither.py <girdi> <çıktı> --width 900` ile işlenir, sonra base64 olarak deck'e gömülür. İşlenmemiş fotoğraf kullanılmaz. Kulüp logosu için `ytu-brand/assets/mark.svg` zaten hazır.

---

## Phase 2: Plan Onayı

**Bu fazda stil üretilmez.** Orijinal skill burada üç stil önizlemesi üretip
kullanıcıya seçtiriyordu; bu depoda tasarım kilitli olduğu için gösterilecek
bir alternatif yok. Onun yerine **içerik planı** onaylanır.

`ytu-brand/design.md` dosyasını şimdi **tamamen** oku.

Kullanıcıya slayt planını sun: her satırda slayt numarası, arketip ve tek
cümlelik içerik.

```
01  Kapak       BLOCKCHAIN 101 — Hafta 01
02  Bölüm       Kriptografik temeller
03  İçerik      Özet fonksiyonu nedir
04  Veri        SHA-256 karşılaştırma tablosu
...
12  Kapanış     Katılım çağrısı
```

Sonra tek soru sor (başlık: "Plan"):
Plan doğru mu? Seçenekler: Onayla / Slayt ekle-çıkar / Sırayı değiştir

Onay gelince Phase 3'e geç.

### Arketip seçimi

Her slayt beş arketipten birine oturur: **Kapak, Bölüm ayracı, İçerik, Veri,
Kapanış**. Tanımları `design.md`'de. Yeni arketip icat etme.

Mavi (`--signal`) yüzey oranını koru: 24 slaytlık deck'te en fazla 4-5 mavi
slayt. Bölüm ayraçları, istatistik slaytları ve kapanış mavi olur; içerik
slaytları koyu kalır.

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

Apply the user's density choice throughout the deck:

- **Low density / speaker-led:** Use more slides with fewer ideas per slide. Favor large headings, short phrases, visual metaphors, section beats, quote/statement slides, and presenter-friendly pacing.
- **High density / reading-first:** Make slides more self-contained. Use structured grids, comparison tables, annotated diagrams, captions, and concise explanatory copy. Keep hierarchy strong so it feels designed, not like a document pasted onto slides.

If the user's stated needs are mixed, choose the closer of the two modes instead of inventing a middle option: live audience persuasion defaults low-density; async circulation or detailed review defaults high-density.

Never let high density become visual clutter. If a high-density slide starts to overflow, split it or redesign it into a clearer structure.

**Üretmeden önce şu dosyaları oku:**

- [ytu-brand/design.md](ytu-brand/design.md) — Tasarım sistemi. Tamamı okunur.
- [html-template.md](html-template.md) — HTML iskeleti ve JS özellikleri
- [viewport-base.css](viewport-base.css) — Zorunlu CSS, tamamı kopyalanır

**Zorunlu kurallar:**

- Tek, kendi kendine yeten HTML dosyası; tüm CSS/JS satır içi.
- `<html lang="tr">` — Türkçe büyük harf dönüşümü için şart.
- `ytu-brand/brand.css` dosyasının **TAM içeriğini** `<style>` bloğuna kopyala.
  Fontlar bu dosyada base64 gömülü; harici font isteği yapma, Google Fonts
  kullanma.
- `viewport-base.css` içeriğini de tam olarak ekle.
- Marka adları ve İngilizce terimler HTML'e elle büyük harf yazılır
  (`BLOCKCHAIN`, `BITCOIN`, `SOLIDITY`, URL'ler). Türkçe kelimeler küçük harf
  yazılıp `text-transform`'a bırakılır.
- Yalnız `design.md`'deki bileşen sınıfları kullanılır. Yeni bileşen gerekiyorsa
  mevcut olanlardan kur; yeni renk veya punto ekleme.
- Her bölüme `/* === BÖLÜM ADI === */` yorum bloğu.

**Üretimden sonra görsel doğrulama yap:** deck'i tarayıcıda aç, ekran görüntüsü
al, metin taşması ve panel çakışması kontrol et. `scrollHeight` kontrolü tek
başına yetmez — bir panel diğerinin üstünü örtebilir ve bu yalnız görselde
fark edilir.

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Plan onayı** — Phase 2'ye geç (stil seçimi yok, yalnız slayt planı)
4. **HTML üret** — Marka sistemine dönüştür; tüm metni, görselleri (assets/ içinden, dither'dan geçirerek), slayt sırasını ve konuşmacı notlarını (HTML yorumu olarak) koru

---

## Phase 5: Delivery

1. **Clean up** — Delete `.frontend-slides/slide-previews/` if it exists
2. **Open** — Use `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - Dosya konumu ve slayt sayısı
   - Navigation: Arrow keys, Space, swipe/tap if enabled
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - Inline text editing is available: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save
   - Offer the natural post-draft actions: ask for revisions, edit text directly in the browser, or export/share

---

## Phase 6: Share & Export (Optional)

After delivery, **ask the user:** _"Would you like to share this presentation? I can deploy it to a live URL (works on any device including phones) or export it as a PDF."_

Options:

- **Deploy to URL** — Shareable link that works on any device
- **Export to PDF** — Universal file for email, Slack, print
- **Both**
- **No thanks**

If the user declines, stop here. If they choose one or both, proceed below.

### 6A: Deploy to a Live URL (Vercel)

This deploys the presentation to Vercel — a free hosting platform. The link works on any device (phones, tablets, laptops) and stays live until the user takes it down.

**If the user has never deployed before, guide them step by step:**

1. **Check if Vercel CLI is installed** — Run `npx vercel --version`. If not found, install Node.js first (`brew install node` on macOS, or download from https://nodejs.org).

2. **Check if user is logged in** — Run `npx vercel whoami`.
   - If NOT logged in, explain: _"Vercel is a free hosting service. You need an account to deploy. Let me walk you through it:"_
     - Step 1: Ask user to go to https://vercel.com/signup in their browser
     - Step 2: They can sign up with GitHub, Google, email — whatever is easiest
     - Step 3: Once signed up, run `vercel login` and follow the prompts (it opens a browser window to authorize)
     - Step 4: Confirm login with `vercel whoami`
   - Wait for the user to confirm they're logged in before proceeding.

3. **Deploy** — Run the deploy script:

   ```bash
   bash scripts/deploy.sh <path-to-presentation>
   ```

   The script accepts either a folder (with index.html) or a single HTML file.

4. **Share the URL** — Tell the user:
   - The live URL (from the script output)
   - That it works on any device — they can text it, Slack it, email it
   - To take it down later: visit https://vercel.com/dashboard and delete the project
   - The Vercel free tier is generous — they won't be charged

**⚠ Deployment gotchas:**

- **Local images/videos must travel with the HTML.** The deploy script auto-detects files referenced via `src="..."` in the HTML and bundles them. But if the presentation references files via CSS `background-image` or unusual paths, those may be missed. **Before deploying, verify:** open the deployed URL and check that all images load. If any are broken, the safest fix is to put the HTML and all its assets into a single folder and deploy the folder instead of a standalone HTML file.
- **Prefer folder deployments when the presentation has many assets.** If the presentation lives in a folder with images alongside it (e.g., `my-deck/index.html` + `my-deck/logo.png`), deploy the folder directly: `bash scripts/deploy.sh ./my-deck/`. This is more reliable than deploying a single HTML file because the entire folder contents are uploaded as-is.
- **Filenames with spaces work but can cause issues.** The script handles spaces in filenames, but Vercel URLs encode spaces as `%20`. If possible, avoid spaces in image filenames. If the user's images have spaces, the script handles it — but if images still break, renaming files to use hyphens instead of spaces is the fix.
- **Redeploying updates the same URL.** Running the deploy script again on the same presentation overwrites the previous deployment. The URL stays the same — no need to share a new link.

### 6B: Export to PDF

This captures each slide as a screenshot and combines them into a PDF. Perfect for email attachments, embedding in documents, or printing.

**Note:** Animations and interactivity are not preserved — the PDF is a static snapshot. This is normal and expected; mention it to the user so they're not surprised.

1. **Run the export script:**

   ```bash
   bash scripts/export-pdf.sh <path-to-html> [output.pdf]
   ```

   If no output path is given, the PDF is saved next to the HTML file.

2. **What happens behind the scenes** (explain briefly to the user):
   - A headless browser opens the presentation at 1920×1080 (standard widescreen)
   - It screenshots each slide one by one
   - All screenshots are combined into a single PDF
   - The script needs Playwright (a browser automation tool) — it will install automatically if missing

3. **If Playwright installation fails:**
   - The most common issue is Chromium not downloading. Run: `npx playwright install chromium`
   - If that fails too, it may be a network/firewall issue. Ask the user to try on a different network.

4. **Deliver the PDF** — The script auto-opens it. Tell the user:
   - The file location and size
   - That it works everywhere — email, Slack, Notion, Google Docs, print
   - Animations are replaced by their final visual state (still looks great, just static)

**⚠ PDF export gotchas:**

- **First run is slow.** The script installs Playwright and downloads a Chromium browser (~150MB) into a temp directory. This happens once per run. Warn the user it may take 30-60 seconds the first time — subsequent exports within the same session are faster.
- **Slides must use `class="slide"`.** The export script finds slides by querying `.slide` elements. If the presentation uses a different class name, the script will report "0 slides found" and fail. All presentations generated by this skill use `.slide`, so this only matters for externally-created HTML.
- **Local images must be loadable via HTTP.** The script starts a local server and loads the HTML through it (so Google Fonts and relative image paths work). If images use absolute filesystem paths (e.g., `src="/Users/name/photo.png"`) instead of relative paths (e.g., `src="photo.png"`), they won't load. Generated presentations always use relative paths, but converted or user-provided decks might not — check and fix if needed.
- **Local images appear in the PDF** as long as they are in the same directory as (or relative to) the HTML file. The export script serves the HTML's parent directory over HTTP, so relative paths like `src="photo.png"` resolve correctly — including filenames with spaces. If images still don't appear, check: (1) the image files actually exist at the referenced path, (2) the paths are relative, not absolute filesystem paths like `/Users/name/photo.png`.
- **Large presentations produce large PDFs.** Each slide is captured as a full 1920×1080 PNG screenshot. An 18-slide deck can produce a ~20MB PDF. If the PDF exceeds 10MB, ask the user: _"The PDF is [size]. Would you like me to compress it? It'll look slightly less sharp but the file will be much smaller."_ If yes, re-run the export with the `--compact` flag:
  ```bash
  bash scripts/export-pdf.sh <path-to-html> [output.pdf] --compact
  ```
  This renders at 1280×720 instead of 1920×1080, typically cutting file size by 50-70% with minimal visual difference.

---

## Supporting Files

| File                                               | Purpose                                                              | When to Read              |
| -------------------------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| [ytu-brand/design.md](ytu-brand/design.md)         | Tasarım sisteminin anayasası — tamamı okunur                    | Phase 2 ve 3              |
| [ytu-brand/brand.css](ytu-brand/brand.css)         | Tokenlar, bileşenler, gömülü fontlar — tamamı kopyalanır         | Phase 3 (üretim)          |
| [ytu-brand/components.html](ytu-brand/components.html) | Canlı bileşen galerisi — görünüm referansı                    | Şüphe hâlinde             |
| [ytu-brand/tools/dither.py](ytu-brand/tools/dither.py) | Fotoğrafı marka diline çevirir                                | Görsel varsa              |
| [viewport-base.css](viewport-base.css)             | Mandatory fixed-stage CSS — copy into every presentation             | Phase 3 (generation)      |
| [html-template.md](html-template.md)               | HTML structure, JS features, code quality standards                  | Phase 3 (generation)      |
| [animation-patterns.md](animation-patterns.md)     | CSS/JS animation snippets and effect-to-feeling guide                | Phase 3 (generation)      |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction                             | Phase 4 (conversion)      |
| [scripts/deploy.sh](scripts/deploy.sh)             | Deploy slides to Vercel for instant sharing                          | Phase 6 (sharing)         |
| [scripts/export-pdf.sh](scripts/export-pdf.sh)     | Export slides to PDF                                                 | Phase 6 (sharing)         |
