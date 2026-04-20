/* ============================================================
   PHIPPS GLOBAL — Interaction Script
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Navbar scroll ──
  const nav = document.getElementById('navbar');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // ── Hamburger ──
  const burger = document.getElementById('burger');
  const mobileMenu = document.getElementById('mobileMenu');
  if (burger && mobileMenu) {
    burger.addEventListener('click', () => {
      mobileMenu.classList.toggle('active');
      document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    });
  }

  // ── Scroll-reveal ──
  const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('active'); observer.unobserve(e.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  reveals.forEach(el => observer.observe(el));

  // ── Counter animation ──
  const counters = document.querySelectorAll('.stat-num');
  const counterObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      const text = el.textContent;
      const match = text.match(/(\d+)/);
      if (!match) return;
      const target = parseInt(match[1]);
      const suffix = text.replace(match[1], '');
      let current = 0;
      const step = Math.max(1, Math.floor(target / 40));
      const interval = setInterval(() => {
        current += step;
        if (current >= target) { current = target; clearInterval(interval); }
        el.textContent = current + suffix;
      }, 30);
      counterObs.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(el => counterObs.observe(el));

  // ── Filter buttons (residential/projects) ──
  const filterBtns = document.querySelectorAll('.filter-btn');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.filter-bar') || btn.parentElement;
      parent.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      const cards = document.querySelectorAll('[data-cat]');
      cards.forEach(card => {
        if (filter === 'all' || card.dataset.cat === filter) {
          card.style.display = '';
          card.style.opacity = '1';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });

  // ── Multi-step form ──
  const typeOpts = document.querySelectorAll('.type-opt');
  typeOpts.forEach(opt => {
    opt.addEventListener('click', () => opt.classList.toggle('sel'));
  });
  const budgetOpts = document.querySelectorAll('.budget-opt');
  budgetOpts.forEach(opt => {
    opt.addEventListener('click', () => {
      budgetOpts.forEach(b => b.classList.remove('sel'));
      opt.classList.add('sel');
    });
  });

  // ── Lightbox ──
  const galleryImgs = document.querySelectorAll('.proj-gallery img');
  if (galleryImgs.length) {
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.innerHTML = '<button class="lightbox-close">×</button><button class="lightbox-prev">‹</button><img src="" alt=""><button class="lightbox-next">›</button>';
    document.body.appendChild(lightbox);
    const lbImg = lightbox.querySelector('img');
    let currentIdx = 0;
    const imgArray = Array.from(galleryImgs);

    galleryImgs.forEach((img, i) => {
      img.addEventListener('click', () => {
        currentIdx = i;
        lbImg.src = img.src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    lightbox.querySelector('.lightbox-close').addEventListener('click', () => {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    });
    lightbox.querySelector('.lightbox-prev').addEventListener('click', () => {
      currentIdx = (currentIdx - 1 + imgArray.length) % imgArray.length;
      lbImg.src = imgArray[currentIdx].src;
    });
    lightbox.querySelector('.lightbox-next').addEventListener('click', () => {
      currentIdx = (currentIdx + 1) % imgArray.length;
      lbImg.src = imgArray[currentIdx].src;
    });
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox) {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  }

  // ── Back to top ──
  const backTop = document.querySelector('.footer-back-top');
  if (backTop) {
    backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // ── Contact form submit ──
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const step3 = document.getElementById('step3');
      if (step3) {
        step3.innerHTML = '<div style="text-align:center;padding:60px 0;"><div style="font-size:48px;margin-bottom:16px;">✓</div><h3 style="margin-bottom:12px;">Thank You!</h3><p>We\'ve received your inquiry and will be in touch within one business day.</p></div>';
        const pills = document.querySelectorAll('.step-pill');
        pills.forEach(p => p.classList.add('done'));
      }
    });
  }

});

// ── Step form navigation ──
function goStep(n) {
  document.querySelectorAll('.form-step').forEach(s => s.classList.remove('active'));
  const target = document.getElementById('step' + n);
  if (target) target.classList.add('active');
  const pills = document.querySelectorAll('.step-pill');
  pills.forEach((p, i) => {
    p.classList.remove('active', 'done');
    if (i < n - 1) p.classList.add('done');
    if (i === n - 1) p.classList.add('active');
  });
}

// ── Accordion toggle ──
function toggleAccordion(btn) {
  const item = btn.closest('.accordion-item');
  const content = item.querySelector('.accordion-content');
  const isOpen = item.classList.contains('active');

  const container = item.closest('.process-accordion');
  container.querySelectorAll('.accordion-item').forEach(fi => {
    fi.classList.remove('active');
    fi.querySelector('.accordion-content').style.maxHeight = '0';
    fi.querySelector('.icon').textContent = '+';
  });

  if (!isOpen) {
    item.classList.add('active');
    content.style.maxHeight = content.scrollHeight + 'px';
    item.querySelector('.icon').textContent = '×';
  }
}

  // ── Hero Testimonial Slider ──
  const heroSlider = document.getElementById('heroTestimonialSlider');
  if (heroSlider) {
    const slides = heroSlider.querySelectorAll('.ht-slide');
    const prevBtn = document.getElementById('htPrev');
    const nextBtn = document.getElementById('htNext');
    let currentSlide = 0;
    let autoSlideInterval;

    function goToSlide(index) {
      slides[currentSlide].classList.remove('active');
      currentSlide = (index + slides.length) % slides.length;
      slides[currentSlide].classList.add('active');
    }

    function nextSlide() { goToSlide(currentSlide + 1); }
    function prevSlide() { goToSlide(currentSlide - 1); }

    if (nextBtn && prevBtn) {
      nextBtn.addEventListener('click', () => { nextSlide(); resetAutoSlide(); });
      prevBtn.addEventListener('click', () => { prevSlide(); resetAutoSlide(); });
    }

    function resetAutoSlide() {
      clearInterval(autoSlideInterval);
      autoSlideInterval = setInterval(nextSlide, 5000);
    }
    resetAutoSlide();
  }

  // ── Portfolio Cards Scroll ──
  const portPrev = document.getElementById('portPrev');
  const portNext = document.getElementById('portNext');
  const portfolioGrid = document.querySelector('.portfolio-grid-4');
  
  if (portPrev && portNext && portfolioGrid) {
    portNext.addEventListener('click', () => {
      portfolioGrid.scrollBy({ left: Math.min(300, window.innerWidth * 0.8), behavior: 'smooth' });
    });
    portPrev.addEventListener('click', () => {
      portfolioGrid.scrollBy({ left: -Math.min(300, window.innerWidth * 0.8), behavior: 'smooth' });
    });
  }
