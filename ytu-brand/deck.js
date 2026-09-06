/* =============================================================================
   YTÜ BLOCKCHAIN — DECK DENETLEYİCİSİ
   -----------------------------------------------------------------------------
   Üç iş yapar: sahneyi pencereye ölçekler, slaytlar arasında gezinir, ilerleme
   çubuklarını kurar. Harici kütüphane yok.

   Bu dosya marka kitinin parçasıdır; deck üretilirken <script> bloğuna olduğu
   gibi gömülür. Deck'e özel davranış buraya yazılmaz.
   ========================================================================== */

(function () {
  'use strict';

  var stage = document.getElementById('deckStage');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  if (!stage || !slides.length) return;

  var index = 0;

  /* --- İlerleme çubukları -------------------------------------------------
     Segment sayısı slayt sayısına eşittir; izleyici kaç slayt kaldığını
     sayabilir. Slayt sayısı HTML'e elle yazılmasın diye buradan doldurulur. */
  document.querySelectorAll('.prog').forEach(function (bar) {
    var total = Number(bar.dataset.total) || slides.length;
    var now = Number(bar.dataset.now) || 0;
    var out = '';
    for (var i = 1; i <= total; i++) {
      out += '<i class="' + (i < now ? 'on' : i === now ? 'now' : '') + '"></i>';
    }
    bar.innerHTML = out;
  });

  /* --- Sahne ölçekleme ----------------------------------------------------
     1920×1080 sahne tek transform ile pencereye sığdırılır ve ortalanır.
     Letterbox/pillarbox olabilir; içerik asla yeniden akmaz.

     Ölçek JavaScript ile hesaplanır çünkü CSS'te yazılamaz:
     `scale(calc(100vw / 1920))` uzunluğu sayıya böler, sonuç yine uzunluk
     olur ve scale() geçersiz sayılıp sessizce yok sayılır. */
  function fit() {
    var scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    var x = (window.innerWidth - 1920 * scale) / 2;
    var y = (window.innerHeight - 1080 * scale) / 2;
    stage.style.transform =
      'translate(' + x + 'px,' + y + 'px) scale(' + scale + ')';
  }

  /* --- Letterbox rengi ----------------------------------------------------
     Ekran oranı 16:9 tutmadığında kalan boşluk aktif slaytın yüzey rengine
     eşitlenir. Sabit koyu bırakılırsa mavi bir slayt ekranın ortasında duran
     bir dikdörtgen gibi görünür ve deck "tam ekran değil" hissi verir. */
  function surfaceOf(slide) {
    if (slide.classList.contains('stage--signal')) return 'var(--signal)';
    if (slide.classList.contains('stage--deep')) return 'var(--deep)';
    return 'var(--void)';
  }

  /* --- Gezinme ------------------------------------------------------------
     Görünürlük `.active`/`.visible` ile yönetilir, `display` ile değil:
     sonradan gelen bir layout kuralı display'i ezip tüm slaytları aynı anda
     görünür yapabilir. */
  function show(next) {
    index = Math.max(0, Math.min(slides.length - 1, next));

    slides.forEach(function (slide, i) {
      slide.classList.toggle('active', i === index);
      slide.classList.toggle('visible', i === index);
    });

    var surface = surfaceOf(slides[index]);
    document.documentElement.style.setProperty('--stage-bg', surface);
    document.documentElement.style.setProperty('--slide-bg', surface);

    if (location.hash !== '#' + (index + 1)) {
      history.replaceState(null, '', '#' + (index + 1));
    }
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      e.preventDefault();
      show(index + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      show(index - 1);
    } else if (e.key === 'Home') {
      show(0);
    } else if (e.key === 'End') {
      show(slides.length - 1);
    } else if (e.key === 'p' || e.key === 'P') {
      /* Tarayıcının yazdırma penceresi. viewport-base.css'teki @media print
         her slaytı ayrı bir sayfaya koyar, oradan PDF'e kaydedilir. */
      window.print();
    }
  });

  /* Dokunmatik: yatay kaydırma slayt değiştirir. 40px eşiği kazara
     dokunuşları eler. */
  var touchX = null;
  document.addEventListener(
    'touchstart',
    function (e) {
      touchX = e.changedTouches[0].clientX;
    },
    { passive: true }
  );
  document.addEventListener(
    'touchend',
    function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 40) show(index + (dx < 0 ? 1 : -1));
      touchX = null;
    },
    { passive: true }
  );

  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', function () {
    var n = parseInt(location.hash.slice(1), 10);
    if (n) show(n - 1);
  });

  fit();
  show(parseInt(location.hash.slice(1), 10) - 1 || 0);
})();
