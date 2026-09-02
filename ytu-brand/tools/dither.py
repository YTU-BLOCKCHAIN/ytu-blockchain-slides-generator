"""
Bir fotografi YTU Blockchain marka dilindeki 1-bit nokta matrisine cevirir.

Marka kitindeki satoshi.png, evolution.png ve banner.png'deki dunya haritasi
hep bu isleme sokulmus goruntuler. Deck'e giren her fotograf ayni islemden
gecmeli; yoksa slayt "markali" durmaz.

Cikti: beyaz noktalar + seffaf zemin. Boylece hem --void hem --signal
zemininde ayni dosya kullanilabilir.

Kullanim:
    python dither.py girdi.png cikti.png [--width 900] [--contrast 1.35]
"""
import argparse

from PIL import Image, ImageEnhance

parser = argparse.ArgumentParser()
parser.add_argument("src")
parser.add_argument("dst")
parser.add_argument("--width", type=int, default=900,
                    help="cikti genisligi; nokta yogunlugunu bu belirler")
parser.add_argument("--contrast", type=float, default=1.35,
                    help="dither oncesi kontrast; yuksek deger daha sert 1-bit")
parser.add_argument("--alpha-threshold", type=int, default=24,
                    help="bu alfa degerinin altindaki pikseller tamamen atilir")
args = parser.parse_args()

src = Image.open(args.src).convert("RGBA")

# Genisligi sabitle. Nokta izgarasi cikti cozunurlugune bagli oldugu icin
# olceklemeyi dither'dan ONCE yapmak sart; sonra olceklemek noktalari bulasik
# gri tonlara cevirir ve 1-bit gorunumu kaybolur.
h = round(src.height * args.width / src.width)
src = src.resize((args.width, h), Image.LANCZOS)

alpha = src.getchannel("A")
gray = src.convert("L")
gray = ImageEnhance.Contrast(gray).enhance(args.contrast)

# convert("1") varsayilan olarak Floyd-Steinberg uygular.
bits = gray.convert("1").convert("L")

# Beyaz noktalari tut, siyahi seffaflastir; orijinal alfayla da maskele ki
# fotografin disindaki alan noktalarla dolmasin.
mask = Image.new("L", src.size, 0)
mask.paste(bits, (0, 0))
mask = Image.composite(mask, Image.new("L", src.size, 0),
                       alpha.point(lambda a: 255 if a > args.alpha_threshold else 0))

out = Image.new("RGBA", src.size, (255, 255, 255, 0))
out.putalpha(mask)
out.paste((255, 255, 255, 255), (0, 0), mask)
out.save(args.dst, optimize=True)

print(f"{args.dst}  {out.size[0]}x{out.size[1]}")
