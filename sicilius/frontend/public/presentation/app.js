/**
 * Sicilius Presentation Slide Deck Engine
 */
document.addEventListener('DOMContentLoaded', () => {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const totalSlides = slides.length;
  let currentSlide = 0;
  let isAutoPlaying = false;
  let autoPlayTimer = null;

  // DOM Elements
  const deckDotsContainer = document.getElementById('deckDots');
  const slideCounter = document.getElementById('slideCounter');
  const progressBar = document.getElementById('progressBar');
  const btnPrev = document.getElementById('btnPrev');
  const btnNext = document.getElementById('btnNext');
  const btnAutoPlay = document.getElementById('btnAutoPlay');
  const btnOverview = document.getElementById('btnOverview');
  const btnFullscreen = document.getElementById('btnFullscreen');
  const overviewModal = document.getElementById('overviewModal');
  const btnCloseOverview = document.getElementById('btnCloseOverview');
  const overviewGrid = document.getElementById('overviewGrid');

  // Initialize Navigation Dots & Overview Grid
  function initDeck() {
    deckDotsContainer.innerHTML = '';
    overviewGrid.innerHTML = '';

    slides.forEach((slide, idx) => {
      // 1. Dots
      const dot = document.createElement('div');
      dot.className = `dot-item ${idx === 0 ? 'active' : ''}`;
      dot.title = `Slayt ${idx + 1}`;
      dot.addEventListener('click', () => goToSlide(idx));
      deckDotsContainer.appendChild(dot);

      // 2. Overview Grid Card
      const titleElem = slide.querySelector('.slide-heading, .slide-title-large');
      const titleText = titleElem ? titleElem.innerText.replace('\n', ' ') : `Slayt ${idx + 1}`;
      const badgeElem = slide.querySelector('.slide-badge, .hero-badge');
      const badgeText = badgeElem ? badgeElem.innerText : `SLİDE ${idx + 1}`;

      const thumb = document.createElement('div');
      thumb.className = `overview-thumb ${idx === 0 ? 'active' : ''}`;
      thumb.innerHTML = `
        <div class="thumb-num">${badgeText}</div>
        <h4>${titleText}</h4>
      `;
      thumb.addEventListener('click', () => {
        goToSlide(idx);
        closeOverview();
      });
      overviewGrid.appendChild(thumb);
    });

    updateUI();
  }

  // Go To Specific Slide
  function goToSlide(index) {
    if (index < 0) index = 0;
    if (index >= totalSlides) index = totalSlides - 1;

    slides.forEach((slide, idx) => {
      slide.classList.remove('active', 'prev-slide');
      if (idx < index) {
        slide.classList.add('prev-slide');
      } else if (idx === index) {
        slide.classList.add('active');
      }
    });

    currentSlide = index;
    updateUI();
    animateSlideNumbers(slides[index]);
  }

  // Animated Number Counter Logic
  function animateSlideNumbers(slideElem) {
    if (!slideElem) return;
    const numElems = slideElem.querySelectorAll('.stat-num, .m-num');
    numElems.forEach(numElem => {
      const originalText = numElem.getAttribute('data-original-text') || numElem.innerText;
      if (!numElem.getAttribute('data-original-text')) {
        numElem.setAttribute('data-original-text', originalText);
      }
      
      // Parse numeric value if present
      const match = originalText.match(/([\d\.,]+)/);
      if (!match) return;
      
      const rawNumStr = match[1].replace(',', '.');
      const targetNum = parseFloat(rawNumStr);
      if (isNaN(targetNum)) return;
      
      const prefix = originalText.substring(0, match.index);
      const suffix = originalText.substring(match.index + match[0].length);
      
      let startNum = 0;
      const duration = 1200; // ms
      const startTime = performance.now();
      
      function step(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const easeVal = 1 - Math.pow(1 - progress, 3);
        const currentVal = (targetNum * easeVal);
        
        let formattedVal = targetNum % 1 !== 0 ? currentVal.toFixed(1) : Math.floor(currentVal).toString();
        numElem.innerText = `${prefix}${formattedVal}${suffix}`;
        
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          numElem.innerText = originalText;
        }
      }
      requestAnimationFrame(step);
    });
  }

  function nextSlide() {
    if (currentSlide < totalSlides - 1) {
      goToSlide(currentSlide + 1);
    } else if (isAutoPlaying) {
      goToSlide(0); // loop if autoplaying
    }
  }

  function prevSlide() {
    if (currentSlide > 0) {
      goToSlide(currentSlide - 1);
    }
  }

  // Update UI Elements
  function updateUI() {
    // Progress Bar
    const progressPct = ((currentSlide + 1) / totalSlides) * 100;
    if (progressBar) progressBar.style.width = `${progressPct}%`;

    // Slide Counter Text
    if (slideCounter) {
      const numStr = (currentSlide + 1).toString().padStart(2, '0');
      const totStr = totalSlides.toString().padStart(2, '0');
      slideCounter.innerText = `SLİDE ${numStr} / ${totStr}`;
    }

    // Dots Active State
    const dots = deckDotsContainer.querySelectorAll('.dot-item');
    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === currentSlide);
    });

    // Overview Thumbs Active State
    const thumbs = overviewGrid.querySelectorAll('.overview-thumb');
    thumbs.forEach((thumb, idx) => {
      thumb.classList.toggle('active', idx === currentSlide);
    });
  }

  // AutoPlay Toggle
  function toggleAutoPlay() {
    isAutoPlaying = !isAutoPlaying;
    if (isAutoPlaying) {
      btnAutoPlay.innerHTML = '<span class="icon">⏸</span> <span class="btn-text">Durdur</span>';
      btnAutoPlay.style.borderColor = 'var(--cyan2)';
      autoPlayTimer = setInterval(nextSlide, 7000);
    } else {
      btnAutoPlay.innerHTML = '<span class="icon">▶</span> <span class="btn-text">Oynat</span>';
      btnAutoPlay.style.borderColor = '';
      clearInterval(autoPlayTimer);
    }
  }

  // Fullscreen Toggle
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.warn('Fullscreen error:', err);
      });
    } else {
      document.exitFullscreen();
    }
  }

  // Overview Modal Controls
  function openOverview() {
    overviewModal.classList.add('active');
  }

  function closeOverview() {
    overviewModal.classList.remove('active');
  }

  // Keyboard Shortcuts
  document.addEventListener('keydown', (e) => {
    // Ignore keypress if modal or input active
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    switch (e.key) {
      case 'ArrowRight':
      case 'ArrowDown':
      case ' ':
      case 'PageDown':
        e.preventDefault();
        nextSlide();
        break;

      case 'ArrowLeft':
      case 'ArrowUp':
      case 'PageUp':
        e.preventDefault();
        prevSlide();
        break;

      case 'Home':
        e.preventDefault();
        goToSlide(0);
        break;

      case 'End':
        e.preventDefault();
        goToSlide(totalSlides - 1);
        break;

      case 'f':
      case 'F':
        e.preventDefault();
        toggleFullscreen();
        break;

      case 'o':
      case 'O':
        e.preventDefault();
        overviewModal.classList.contains('active') ? closeOverview() : openOverview();
        break;

      case 'Escape':
        closeOverview();
        break;
    }
  });

  // Touch Swipe Gestures
  let touchStartX = 0;
  let touchEndX = 0;
  const viewport = document.getElementById('deckViewport');

  viewport.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, false);

  viewport.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, false);

  function handleSwipe() {
    const diffX = touchEndX - touchStartX;
    if (Math.abs(diffX) > 50) {
      if (diffX < 0) {
        nextSlide(); // Swipe Left -> Next
      } else {
        prevSlide(); // Swipe Right -> Prev
      }
    }
  }

  // FAQ Accordion Listeners
  document.querySelectorAll('.faq-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('open');
    });
  });

  // Event Listeners
  if (btnPrev) btnPrev.addEventListener('click', prevSlide);
  if (btnNext) btnNext.addEventListener('click', nextSlide);
  if (btnAutoPlay) btnAutoPlay.addEventListener('click', toggleAutoPlay);
  if (btnOverview) btnOverview.addEventListener('click', openOverview);
  if (btnCloseOverview) btnCloseOverview.addEventListener('click', closeOverview);
  if (btnFullscreen) btnFullscreen.addEventListener('click', toggleFullscreen);

  // Initialize
  initDeck();
});
