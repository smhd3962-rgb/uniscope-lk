// Mobile menu toggle
function toggleMobileMenu() {
  const mobileMenu = document.getElementById('mobileMenu');
  const menuIcon = document.getElementById('menuIcon');
  const closeIcon = document.getElementById('closeIcon');
  
  if (!mobileMenu) return;
  mobileMenu.classList.toggle('show');
  if (menuIcon) menuIcon.classList.toggle('hidden');
  if (closeIcon) closeIcon.classList.toggle('hidden');
}

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  if (!mobileMenu || !mobileMenuBtn) return;
  
  if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
    mobileMenu.classList.remove('show');
    const menuIcon = document.getElementById('menuIcon');
    const closeIcon = document.getElementById('closeIcon');
    if (menuIcon) menuIcon.classList.remove('hidden');
    if (closeIcon) closeIcon.classList.add('hidden');
  }
});

// Accordion toggle for feature menu
function toggleAccordion(button) {
  const accordion = button.closest('.feature-accordion');
  if (accordion) accordion.classList.toggle('open');
}

// User dropdown toggle
function toggleUserDropdown() {
  const dropdown = document.getElementById('userDropdown');
  if (dropdown) {
    dropdown.classList.toggle('show');
  }
}

// Close user dropdown when clicking outside
document.addEventListener('click', function(e) {
  const dropdown = document.getElementById('userDropdown');
  const btn = document.querySelector('.user-avatar-btn');
  if (dropdown && btn && !dropdown.contains(e.target) && !btn.contains(e.target)) {
    dropdown.classList.remove('show');
  }
});

// ── Apple-Style Scroll Reveal & Micro-Interactions ──
document.addEventListener('DOMContentLoaded', function() {
  // Check prefers-reduced-motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal elements on scroll
  if (!prefersReducedMotion && 'IntersectionObserver' in window) {
    const revealTargets = document.querySelectorAll('.apple-reveal, .tool-card, .feature-card, .uniscope-card');
    const revealObserver = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '0px 0px -40px 0px',
      threshold: 0.1
    });

    revealTargets.forEach(target => {
      target.style.transition = 'opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
      if (!target.classList.contains('is-revealed')) {
        target.style.opacity = '0';
        target.style.transform = 'translateY(16px)';
      }
      revealObserver.observe(target);
    });

    // Animate stats bar numbers
    const statsBar = document.querySelector('.hs-bar');
    if (statsBar) {
      const statsObserver = new IntersectionObserver((entries, obs) => {
        if (entries[0].isIntersecting) {
          document.querySelectorAll('.hs-num').forEach(el => {
            const target = parseInt(el.getAttribute('data-t'), 10);
            const suffix = el.getAttribute('data-s') || '';
            const affix = el.getAttribute('data-a') || '';
            if (isNaN(target)) return;

            const duration = 1200;
            const startTime = performance.now();
            function updateNumber(now) {
              const elapsed = now - startTime;
              const progress = Math.min(elapsed / duration, 1);
              // Apple smooth cubic ease-out
              const easeProgress = 1 - Math.pow(1 - progress, 3);
              const current = Math.floor(easeProgress * target);
              el.textContent = current + suffix + affix;
              if (progress < 1) {
                requestAnimationFrame(updateNumber);
              } else {
                el.textContent = target + suffix + affix;
              }
            }
            requestAnimationFrame(updateNumber);
          });
          obs.unobserve(statsBar);
        }
      }, { threshold: 0.2 });
      statsObserver.observe(statsBar);
    }
  }

  // Keyboard shortcut: cmd/ctrl+K to focus search input
  document.addEventListener('keydown', function(e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      const searchInput = document.querySelector('.hero-search-form input, #degreeSearch, #searchInput');
      if (searchInput) {
        e.preventDefault();
        searchInput.focus();
      }
    }
  });
});

// Helper for revealed class
document.head.insertAdjacentHTML('beforeend', '<style>.is-revealed { opacity: 1 !important; transform: translateY(0) !important; }</style>');
