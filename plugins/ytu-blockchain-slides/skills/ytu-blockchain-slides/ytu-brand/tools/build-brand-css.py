"""
brand.src.css icindeki font yer tutucularini base64 ile doldurup kendi kendine
yeten brand.css'i uretir.

Deck'ler tek HTML dosyasi olarak dagitiliyor; harici font istegi olamaz, cunku
sunum sirasinda ag baglantisi garanti degil ve Google Fonts'ta olmayan bir
marka fontu kullaniyoruz. Toplam gomulu yuk ~69 KB.

Kullanim:
    python tools/build-brand-css.py
"""
import base64
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "brand.src.css"
OUT = ROOT / "brand.css"

FONTS = {
    "{{FONT_VHS}}": ROOT / "fonts" / "eas-vhs-tr.woff2",
    "{{FONT_CLASH}}": ROOT / "fonts" / "clash-grotesk-variable.woff2",
}

css = SRC.read_text(encoding="utf-8")

for token, path in FONTS.items():
    if token not in css:
        raise SystemExit(f"yer tutucu bulunamadi: {token}")
    css = css.replace(token, base64.b64encode(path.read_bytes()).decode("ascii"))

header = (
    "/* URETILMIS DOSYA -- elle duzenlemeyin.\n"
    "   Kaynak: brand.src.css  |  Uretim: tools/build-brand-css.py */\n"
)
OUT.write_text(header + css, encoding="utf-8")

print(f"{OUT.relative_to(ROOT)}  {len(OUT.read_bytes()) / 1024:.0f} KB")
