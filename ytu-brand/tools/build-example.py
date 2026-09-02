"""
examples/ornek-deck.src.html'den kendi kendine yeten ornek deck'i uretir.

Bu dosyanin asil isi referans deck vermek degil, ENTEGRASYONU KANITLAMAK:
brand.css ile viewport-base.css ayni sayfada dogru calisiyor mu, fontlar
gomuluyor mu, dither gorseller yerine oturuyor mu. Galeriye bakarak bunlarin
hicbiri anlasilmaz cunku galeride `.slide` sinifi hic yok.

Kullanim:
    python tools/build-example.py
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent   # ytu-brand/
REPO = ROOT.parent
SRC = REPO / "examples" / "ornek-deck.src.html"
OUT = REPO / "examples" / "ornek-deck.html"

if not (ROOT / "brand.css").exists():
    raise SystemExit("once tools/build-brand-css.py calistirin")


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


html = SRC.read_text(encoding="utf-8")

replacements = {
    "{{BRAND_CSS}}": (ROOT / "brand.css").read_text(encoding="utf-8"),
    "{{VIEWPORT_CSS}}": (REPO / "viewport-base.css").read_text(encoding="utf-8"),
    "{{MARK}}": data_uri(ROOT / "assets" / "mark.svg", "image/svg+xml"),
    "{{SATOSHI}}": data_uri(ROOT / "assets" / "satoshi-1bit.png", "image/png"),
    "{{EVOLUTION}}": data_uri(ROOT / "assets" / "evolution-1bit.png", "image/png"),
}

for token, value in replacements.items():
    if token not in html:
        raise SystemExit(f"yer tutucu bulunamadi: {token}")
    html = html.replace(token, value)

OUT.write_text(html, encoding="utf-8")
print(f"{OUT.relative_to(REPO)}  {len(OUT.read_bytes()) / 1024:.0f} KB")
