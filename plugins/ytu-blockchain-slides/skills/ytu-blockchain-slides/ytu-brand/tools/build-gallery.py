"""
components.src.html icindeki yer tutuculari doldurup kendi kendine yeten
components.html'i uretir.

Galeri tek dosya olmali: tarayicida dogrudan acilabilsin, paylasilabilsin ve
deck'lerin gercek davranisiyla ayni kosullarda (harici istek yok) render
edilsin diye.

Kullanim:
    python tools/build-brand-css.py && python tools/build-gallery.py
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "components.src.html"
OUT = ROOT / "components.html"
CSS = ROOT / "brand.css"

if not CSS.exists():
    raise SystemExit("once tools/build-brand-css.py calistirin")


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


html = SRC.read_text(encoding="utf-8")

# brand.css icinde $ ve \ yok ama str.replace kullandigimiz icin kacis
# gerekmiyor; yine de tek seferde ve acikca degistiriyoruz.
replacements = {
    "{{BRAND_CSS}}": CSS.read_text(encoding="utf-8"),
    "{{MARK}}": data_uri(ROOT / "assets" / "mark.svg", "image/svg+xml"),
    "{{SATOSHI}}": data_uri(ROOT / "assets" / "satoshi-1bit.png", "image/png"),
    "{{EVOLUTION}}": data_uri(ROOT / "assets" / "evolution-1bit.png", "image/png"),
}

for token, value in replacements.items():
    if token not in html:
        raise SystemExit(f"yer tutucu bulunamadi: {token}")
    html = html.replace(token, value)

OUT.write_text(html, encoding="utf-8")
print(f"{OUT.relative_to(ROOT)}  {len(OUT.read_bytes()) / 1024:.0f} KB")
