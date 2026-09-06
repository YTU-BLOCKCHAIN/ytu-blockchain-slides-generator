# =============================================================================
# YTÜ BLOCKCHAIN SLIDES GENERATOR
# -----------------------------------------------------------------------------
# Üretilmiş dosyalar depoda tutulmaz (bkz. .gitignore). Klonladıktan sonra
# `make` demek yeterli.
# =============================================================================

PY := python3
BRAND := ytu-brand

.PHONY: all kur brand galeri ornek kit temiz font

all: brand galeri ornek           ## Her şeyi üret

kur:                              ## Python bağımlılıkları
	$(PY) -m pip install --user fonttools brotli Pillow

brand:                            ## brand.src.css + fontlar -> brand.css
	cd $(BRAND) && $(PY) tools/build-brand-css.py

galeri: brand                     ## Bileşen galerisi
	cd $(BRAND) && $(PY) tools/build-gallery.py

ornek: brand                      ## Örnek deck
	cd $(BRAND) && $(PY) tools/build-example.py

# -----------------------------------------------------------------------------
# MARKA KİTİ
# `slides` deposunun ihtiyaç duyduğu her şeyi dist/kit/ altına toplar.
# Oradan `slides` deposundaki brand/ klasörüne kopyalanır.
#
# Kitin içinde kaynak dosya yoktur: brand.src.css, fontlar ve tools/ burada
# kalır. Deck yazan kişinin bunlara erişmesi gerekmiyor.
# -----------------------------------------------------------------------------
kit: brand                        ## slides deposu için marka kiti üret
	@rm -rf dist/kit && mkdir -p dist/kit/assets
	@cp $(BRAND)/brand.css        dist/kit/
	@cp $(BRAND)/deck.js          dist/kit/
	@cp $(BRAND)/design.md        dist/kit/
	@cp viewport-base.css         dist/kit/
	@cp $(BRAND)/assets/mark.svg  dist/kit/assets/
	@git rev-parse --short HEAD > dist/kit/VERSION
	@echo "dist/kit/ hazır — $$(du -sh dist/kit | cut -f1)"
	@ls -1 dist/kit

font:                             ## EAS VHS'i yeniden yamala (Drive'daki orijinalden)
	cd $(BRAND) && $(PY) tools/patch-eas-vhs.py \
	  "$$HOME/contact@ytublockchain.com - Google Drive/My Drive/design/font/primary-eas-vhs.ttf" \
	  fonts/eas-vhs-tr.ttf
	cd $(BRAND) && $(PY) -c "from fontTools.ttLib import TTFont; \
	  f=TTFont('fonts/eas-vhs-tr.ttf'); f.flavor='woff2'; \
	  f.save('fonts/eas-vhs-tr.woff2')"

temiz:                            ## Üretilmiş dosyaları sil
	rm -rf dist $(BRAND)/brand.css $(BRAND)/components.html examples/ornek-deck.html
