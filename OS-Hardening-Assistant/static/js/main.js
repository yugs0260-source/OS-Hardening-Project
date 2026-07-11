/* ============================================================
   main.js — Global JavaScript for OS Hardening Assistant
   ============================================================ */

'use strict';

// ──────────────────────────────────────────────
// Navbar active state
// ──────────────────────────────────────────────
(function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    const href = item.getAttribute('href');
    if (href && (path === href || (href !== '/' && path.startsWith(href)))) {
      item.classList.add('active');
    }
  });
})();

// ──────────────────────────────────────────────
// Toast notification system
// ──────────────────────────────────────────────
const Toast = {
  container: null,

  init() {
    this.container = document.querySelector('.toast-container');
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },

  show(message, type = 'info', duration = 3500) {
    if (!this.container) this.init();

    const icons = {
      success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><polyline points="20 6 9 17 4 12"/></svg>`,
      error:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
      warning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
      info:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span style="color:var(--accent-${type === 'success' ? 'green' : type === 'error' ? 'red' : type === 'warning' ? 'yellow' : 'cyan'})">${icons[type] || icons.info}</span>${message}`;
    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slide-in 0.3s ease reverse';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  success(msg) { this.show(msg, 'success'); },
  error(msg)   { this.show(msg, 'error'); },
  warning(msg) { this.show(msg, 'warning'); },
  info(msg)    { this.show(msg, 'info'); },
};

// ──────────────────────────────────────────────
// Copy to Clipboard
// ──────────────────────────────────────────────
function copyToClipboard(text) {
  navigator.clipboard.writeText(text)
    .then(() => Toast.success('Copied to clipboard!'))
    .catch(() => {
      // Fallback
      const el = document.createElement('textarea');
      el.value = text;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      Toast.success('Copied to clipboard!');
    });
}

// ──────────────────────────────────────────────
// Copy button for code blocks
// ──────────────────────────────────────────────
document.querySelectorAll('.code-block').forEach(block => {
  const copyBtn = block.querySelector('.copy-btn');
  if (!copyBtn) return;

  copyBtn.addEventListener('click', () => {
    const code = block.querySelector('pre');
    if (code) copyToClipboard(code.innerText);
  });
});

// ──────────────────────────────────────────────
// Script download helper
// ──────────────────────────────────────────────
function downloadScript(content, filename) {
  const blob = new Blob([content], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  Toast.success(`Downloaded ${filename}`);
}

// ──────────────────────────────────────────────
// Animate numbers (counter effect)
// ──────────────────────────────────────────────
function animateNumber(el, target, duration = 1200) {
  const start = 0;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
    el.textContent = Math.round(start + (target - start) * ease);
    if (progress < 1) requestAnimationFrame(update);
  }

  requestAnimationFrame(update);
}

// ──────────────────────────────────────────────
// Intersection Observer for fade-in animations
// ──────────────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card, .check-card, .score-section').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// ──────────────────────────────────────────────
// Expose globals
// ──────────────────────────────────────────────
window.Toast = Toast;
window.copyToClipboard = copyToClipboard;
window.downloadScript = downloadScript;
window.animateNumber = animateNumber;
