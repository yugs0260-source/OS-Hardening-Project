/* ============================================================
   dashboard.js — Dashboard AJAX refresh and score animation
   ============================================================ */

'use strict';

// ──────────────────────────────────────────────
// Score Ring Animation
// ──────────────────────────────────────────────
function initScoreRing() {
  const ring = document.querySelector('.score-ring-fill');
  const scoreEl = document.querySelector('.score-number');
  if (!ring || !scoreEl) return;

  const score = parseInt(scoreEl.dataset.score || scoreEl.textContent, 10);
  const circumference = 440; // 2 * π * r (r=70)
  const offset = circumference - (score / 100) * circumference;

  // Set grade class
  const gradeClasses = { A: 'grade-a', B: 'grade-b', C: 'grade-c', D: 'grade-d', F: 'grade-f' };
  const grade = scoreEl.dataset.grade || 'F';
  ring.classList.add(gradeClasses[grade] || 'grade-f');

  // Animate after slight delay
  setTimeout(() => {
    ring.style.strokeDashoffset = offset;
  }, 300);

  // Animate number
  if (window.animateNumber) {
    scoreEl.textContent = '0';
    setTimeout(() => window.animateNumber(scoreEl, score), 300);
  }
}

// ──────────────────────────────────────────────
// AJAX Status Refresh
// ──────────────────────────────────────────────
function refreshStatus(checkName) {
  const btn = document.querySelector(`[data-refresh="${checkName}"]`);
  if (btn) {
    btn.classList.add('loading');
    btn.disabled = true;
  }

  fetch(`/api/check-status/?check=${encodeURIComponent(checkName)}`)
    .then(res => res.json())
    .then(data => {
      if (data.result) {
        updateCheckCard(checkName, data.result);
        window.Toast && window.Toast.success(`${checkName} status refreshed`);
      }
    })
    .catch(() => {
      window.Toast && window.Toast.error('Could not refresh status. Is the server running?');
    })
    .finally(() => {
      if (btn) {
        btn.classList.remove('loading');
        btn.disabled = false;
      }
    });
}

function refreshAllStatus() {
  const btn = document.getElementById('btn-refresh-all');
  if (btn) { btn.classList.add('loading'); btn.disabled = true; }

  fetch('/api/check-status/?check=all')
    .then(res => res.json())
    .then(data => {
      if (data.results) {
        Object.entries(data.results).forEach(([key, result]) => {
          updateCheckCard(key, result);
        });
        // Update score
        if (data.score !== undefined) {
          const scoreEl = document.querySelector('.score-number');
          if (scoreEl && window.animateNumber) {
            window.animateNumber(scoreEl, data.score);
          }
        }
        window.Toast && window.Toast.success('All statuses refreshed!');
      }
    })
    .catch(() => {
      window.Toast && window.Toast.error('Refresh failed. Check server connectivity.');
    })
    .finally(() => {
      if (btn) { btn.classList.remove('loading'); btn.disabled = false; }
    });
}

function updateCheckCard(name, result) {
  const card = document.querySelector(`[data-check="${name}"]`);
  if (!card) return;

  // Update status class
  card.className = `check-card ${result.status}`;

  // Update badge
  const badge = card.querySelector('.badge');
  if (badge) {
    badge.className = `badge badge-${result.status}`;
    const labels = { secure: '✓ Secure', warning: '⚠ Warning', danger: '✗ Danger', unknown: '? Unknown' };
    badge.textContent = labels[result.status] || result.status;
  }

  // Update detail text
  const detail = card.querySelector('.check-card-detail');
  if (detail) detail.textContent = result.detail;

  // Update score bar
  const scoreBar = card.querySelector('.check-card-score-fill');
  if (scoreBar) scoreBar.style.width = `${result.score}%`;

  const scoreNum = card.querySelector('.check-card-score-num');
  if (scoreNum) scoreNum.textContent = result.score;
}

// ──────────────────────────────────────────────
// Init
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initScoreRing();

  // Wire refresh buttons
  document.getElementById('btn-refresh-all')?.addEventListener('click', refreshAllStatus);

  document.querySelectorAll('[data-refresh]').forEach(btn => {
    btn.addEventListener('click', () => refreshStatus(btn.dataset.refresh));
  });
});

window.refreshAllStatus = refreshAllStatus;
window.refreshStatus = refreshStatus;
