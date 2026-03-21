/**
 * Diamond Hill Resort — Luxury Interactions
 * Scroll reveal, parallax, navbar, hero slideshow, counters
 */

document.addEventListener('DOMContentLoaded', () => {
  // ── 1. Scroll Reveal ──────────────────────────────
  const revealElements = document.querySelectorAll(
    '.reveal, .reveal-left, .reveal-right, .stagger-children'
  );

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );

  revealElements.forEach((el) => revealObserver.observe(el));

  // Auto-apply reveal to major sections
  document.querySelectorAll('section > .container, .page-header-content').forEach((el) => {
    if (!el.classList.contains('reveal') &&
        !el.classList.contains('reveal-left') &&
        !el.classList.contains('reveal-right')) {
      el.classList.add('reveal');
      revealObserver.observe(el);
    }
  });

  // ── 2. Navbar Scroll Effect ────────────────────────
  const navbar = document.querySelector('.navbar-premium');
  if (navbar) {
    const onScroll = () => {
      if (window.scrollY > 60) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── 3. Hero Slideshow ──────────────────────────────
  const slides = document.querySelectorAll('.hero-slideshow .slide');
  const slideTexts = document.querySelectorAll('.hero-slide-text');

  if (slides.length > 1) {
    let currentSlide = 0;

    // Activate first slide
    if (slides[0]) slides[0].classList.add('active');

    const nextSlide = () => {
      slides[currentSlide].classList.remove('active');
      if (slideTexts[currentSlide]) slideTexts[currentSlide].style.display = 'none';

      currentSlide = (currentSlide + 1) % slides.length;

      slides[currentSlide].classList.add('active');
      if (slideTexts[currentSlide]) {
        slideTexts[currentSlide].style.display = 'block';
        // Animate text in
        slideTexts[currentSlide].style.opacity = '0';
        slideTexts[currentSlide].style.transform = 'translateY(20px)';
        requestAnimationFrame(() => {
          slideTexts[currentSlide].style.transition = 'all 0.8s cubic-bezier(0.22,1,0.36,1)';
          slideTexts[currentSlide].style.opacity = '1';
          slideTexts[currentSlide].style.transform = 'translateY(0)';
        });
      }
    };

    setInterval(nextSlide, 5500);
  } else if (slides.length === 1) {
    slides[0].classList.add('active');
  }

  // ── 4. Smooth Scroll for Anchor Links ───────────────
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── 5. Image Lazy-load Placeholder Fade ─────────────
  document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
    img.style.opacity = '0';
    img.style.transition = 'opacity 0.6s ease';
    if (img.complete) {
      img.style.opacity = '1';
    } else {
      img.addEventListener('load', () => { img.style.opacity = '1'; });
    }
  });

  // ── 6. Counter Animation ────────────────────────────
  const counters = document.querySelectorAll('.stat-value[data-count]');
  const counterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const target = parseInt(el.dataset.count, 10);
          const suffix = el.dataset.suffix || '';
          let counter = 0;
          const step = Math.max(1, Math.ceil(target / 60));
          const interval = setInterval(() => {
            counter += step;
            if (counter >= target) {
              counter = target;
              clearInterval(interval);
            }
            el.textContent = counter + suffix;
          }, 25);
          counterObserver.unobserve(el);
        }
      });
    },
    { threshold: 0.5 }
  );
  counters.forEach((el) => counterObserver.observe(el));

  // ── 7. Review Carousel (if multiple pages) ──────────
  const reviewDots = document.querySelectorAll('.carousel-dot');
  const reviewContainer = document.getElementById('reviewsCarousel');

  if (reviewDots.length > 0 && reviewContainer) {
    reviewDots.forEach((dot) => {
      dot.addEventListener('click', () => {
        const index = parseInt(dot.dataset.slideIndex, 10);
        const offset = -index * 100;
        reviewContainer.style.transform = `translateX(${offset}%)`;

        reviewDots.forEach((d) => d.classList.remove('active'));
        dot.classList.add('active');
      });
    });

    // Auto-advance reviews
    let currentReviewPage = 0;
    setInterval(() => {
      currentReviewPage = (currentReviewPage + 1) % reviewDots.length;
      reviewDots[currentReviewPage].click();
    }, 6000);
  }

  // ── 8. Star Rating Interactive (Review Modal) ───────
  const starRating = document.getElementById('starRating');
  if (starRating) {
    const stars = starRating.querySelectorAll('.fas.fa-star');
    const ratingInput = document.getElementById('reviewRatingValue');

    stars.forEach((star) => {
      star.addEventListener('mouseenter', () => {
        const rating = parseInt(star.dataset.rating, 10);
        stars.forEach((s, i) => {
          s.style.color = i < rating ? '#c9a84c' : '#ddd';
        });
      });

      star.addEventListener('click', () => {
        const rating = parseInt(star.dataset.rating, 10);
        if (ratingInput) ratingInput.value = rating;
        stars.forEach((s, i) => {
          s.style.color = i < rating ? '#c9a84c' : '#ddd';
        });
      });
    });

    starRating.addEventListener('mouseleave', () => {
      const current = parseInt(ratingInput?.value || '0', 10);
      stars.forEach((s, i) => {
        s.style.color = i < current ? '#c9a84c' : '#ddd';
      });
    });
  }

  // ── 9. Parallax on Hero (subtle) ────────────────────
  const heroSection = document.querySelector('.hero-section');
  if (heroSection) {
    window.addEventListener('scroll', () => {
      const scrollPos = window.scrollY;
      if (scrollPos < window.innerHeight) {
        const translateValue = scrollPos * 0.3;
        const slideEls = heroSection.querySelectorAll('.slide');
        slideEls.forEach((s) => {
          s.style.transform = `translateY(${translateValue}px) scale(1.05)`;
        });
      }
    }, { passive: true });
  }

  // ── 10. Booking Date Validation ─────────────────────
  const checkinInput = document.getElementById('checkin') || document.getElementById('id_check_in');
  const checkoutInput = document.getElementById('checkout') || document.getElementById('id_check_out');

  if (checkinInput && checkoutInput) {
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    checkinInput.setAttribute('min', today);

    checkinInput.addEventListener('change', () => {
      const checkinDate = new Date(checkinInput.value);
      checkinDate.setDate(checkinDate.getDate() + 1);
      const minCheckout = checkinDate.toISOString().split('T')[0];
      checkoutInput.setAttribute('min', minCheckout);

      if (checkoutInput.value && checkoutInput.value <= checkinInput.value) {
        checkoutInput.value = minCheckout;
      }
    });
  }

  // ── 11. Form Validation Feedback ────────────────────
  document.querySelectorAll('.needs-validation').forEach((form) => {
    form.addEventListener('submit', (e) => {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });

  console.log('✨ Diamond Hill Resort — Luxury UI loaded');
});
