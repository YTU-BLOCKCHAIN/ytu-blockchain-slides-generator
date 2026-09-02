"""
EAS VHS'e eksik Turkce harfleri ekler: G-breve, I-dot, S-cedilla (buyuk/kucuk).

Font 2048 upem uzerinde 120.5 birimlik yarim-piksel izgarasina oturuyor
(tam piksel = 241). Cap height 1686 (7px), x-height 1204 (5px).
Aksan bolgeleri fontun kendi orneklerinden okundu:
  - buyuk harf aksani  : y 1807..2048 (Idieresis), 2 sirali 2288'e kadar (Aring)
  - kucuk harf aksani  : y 1445..1686 (i noktasi)
  - sedilla            : Ccedilla icinde x +240 kaydirilmis
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Offset

SRC, DST = sys.argv[1], sys.argv[2]

PX = 241          # tam piksel
HALF = 120.5      # izgara adimi
CAP = 1686        # buyuk harf yuksekligi
XH = 1204         # kucuk harf yuksekligi
CAP_ACC = 1807    # buyuk harf aksaninin alt kenari
LC_ACC = 1445     # kucuk harf aksaninin alt kenari

font = TTFont(SRC)
glyf = font["glyf"]
hmtx = font["hmtx"]


def record(name):
    """Bir glifin cizim komutlarini kaydeder."""
    pen = RecordingPen()
    glyf[name].draw(pen, glyf)
    return pen.value


def rect(pen, x0, y0, x1, y1):
    """Piksel fontuna uygun duz dikdortgen kontur."""
    pen.moveTo((round(x0), round(y0)))
    pen.lineTo((round(x1), round(y0)))
    pen.lineTo((round(x1), round(y1)))
    pen.lineTo((round(x0), round(y1)))
    pen.closePath()


def breve(pen, x0, x1, y0):
    """
    Kap seklinde piksel breve:
        #  .  #     ust sira, iki uctaki hucreler
        #  #  #     alt sira, tam genislik

    Siralar TAM degil YARIM piksel (120.5 birim) yuksekliginde. Toplam yukseklik
    boylece 241 = 1 piksel olur ve breve, fontun kendi aksan bandina (buyuk
    harfte 1807-2048) sigar.

    Tam piksel siralarla yapilan ilk surum 2289'a, yani 1.118 em'e cikiyordu --
    fontun dogal tavani olan 1.000 em'in (I noktasinin tepesi) uzerine. Sonuc:
    "01 / DEGISTIRILEMEZ" gibi yiginlarda breve bir ust satira giriyor ve
    cakismayi onlemek icin tum satir yuksekliklerini gereksiz yere acmak
    gerekiyordu. Yarim piksel izgarasi fontun kendi olcusu (sedilla da 120
    birimlik bir kare kullaniyor), o yuzden kap sekli bozulmadan kuculuyor.
    """
    row = HALF
    rect(pen, x0, y0, x1, y0 + row)                       # alt bar
    rect(pen, x0, y0 + row, x0 + PX, y0 + 2 * row)        # sol ust
    rect(pen, x1 - PX, y0 + row, x1, y0 + 2 * row)        # sag ust


CEDILLA = record("cedilla")


def compose(base, extras, advance):
    """Taban glifi + ek konturlardan yeni bir glif uretir."""
    pen = TTGlyphPen(glyf)
    for cmd, args in record(base):
        getattr(pen, cmd)(*args)
    extras(pen)
    return pen.glyph(), advance


def add_cedilla(pen):
    """Sedillayi Ccedilla'daki ile ayni yere (+240) koyar."""
    tp = TransformPen(pen, Offset(240, 0))
    for cmd, args in CEDILLA:
        getattr(tp, cmd)(*args)


new = {}

# S-cedilla / s-cedilla -- sedilla hazir parca, Ccedilla'daki konumla ayni
new["Scedilla"] = compose("S", add_cedilla, hmtx["S"][0])
new["scedilla"] = compose("s", add_cedilla, hmtx["s"][0])

# I-dot -- nokta, I'nin (722 genislik) tam ortasina, buyuk harf aksan seviyesine
new["Idotaccent"] = compose(
    "I",
    lambda p: rect(p, 240, CAP_ACC, 240 + PX, CAP_ACC + PX),
    hmtx["I"][0],
)

# G-breve -- 3px genislikte breve, G'nin (963 genislik) ustunde ortalanmis
new["Gbreve"] = compose(
    "G",
    lambda p: breve(p, 120, 120 + 3 * PX, CAP_ACC),
    hmtx["G"][0],
)

# g-breve -- ayni breve, kucuk harf aksan seviyesinde
new["gbreve"] = compose(
    "g",
    lambda p: breve(p, 120, 120 + 3 * PX, LC_ACC),
    hmtx["g"][0],
)

for name, (glyph, adv) in new.items():
    glyf[name] = glyph
    glyph.recalcBounds(glyf)
    hmtx[name] = (adv, glyph.xMin)

# glyf.__setitem__ yeni adi zaten glyphOrder'a ekliyor; fontun kendi sirasini
# ona esitlemek yeterli.
font.setGlyphOrder(glyf.glyphOrder)

# --- Tabular rakamlar ------------------------------------------------------
# Ne EAS VHS'te ne de Clash Grotesk'te tnum ozelligi var. Sayfa sayaci
# (01/24 -> 11/24), tablo sutunlari ve istatistik bloklari icin rakamlarin
# ayni genislikte olmasi sart; hepsini en genis rakama (1234) esitleyip
# glifi yarim-piksel izgarasina oturarak ortaliyoruz.
_cmap = font.getBestCmap()
digits = [_cmap[ord(c)] for c in "0123456789"]
slot = max(hmtx[n][0] for n in digits)
for name in digits:
    adv = hmtx[name][0]
    g = glyf[name]
    g.expand(glyf)
    steps = int(((slot - adv) / 2) / HALF + 0.5)
    shift = int(steps * HALF)
    if shift:
        g.coordinates.translate((shift, 0))
    g.recalcBounds(glyf)
    hmtx[name] = (slot, g.xMin)
print("tabular rakam yuvasi:", slot)

CODEPOINTS = {
    0x011E: "Gbreve",
    0x011F: "gbreve",
    0x0130: "Idotaccent",
    0x015E: "Scedilla",
    0x015F: "scedilla",
}
for table in font["cmap"].tables:
    if table.isUnicode():
        table.cmap.update(CODEPOINTS)

# Yeni glifler mevcut ust sinirin (Aring, 2288) altinda kaliyor ama yine de
# head/hhea kutularini yeniden hesaplat.
font["head"].yMax = max(font["head"].yMax, max(g.yMax for g in (glyf[n] for n in new)))

font["name"].setName("EAS VHS TR", 1, 3, 1, 0x409)
font["name"].setName("EAS VHS TR Regular", 4, 3, 1, 0x409)

font.save(DST)

check = TTFont(DST).getBestCmap()
missing = [c for c in "ÇĞİÖŞÜçğıöşü" if ord(c) not in check]
print("kaydedildi:", DST)
print("eksik kalan:", "".join(missing) or "(yok)")
for cp, nm in CODEPOINTS.items():
    g = TTFont(DST)["glyf"][nm]
    print(f"  U+{cp:04X} {chr(cp)}  konturlar={g.numberOfContours}  "
          f"bbox=({g.xMin},{g.yMin},{g.xMax},{g.yMax})")
