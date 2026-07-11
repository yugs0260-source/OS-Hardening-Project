/* ============================================================
   checklist.js — Interactive hardening checklist with localStorage
   ============================================================ */

'use strict';

const STORAGE_KEY = 'osh-checklist';

// ──────────────────────────────────────────────
// Load/Save State
// ──────────────────────────────────────────────
function loadState() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  } catch {
    return {};
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

// ──────────────────────────────────────────────
// Progress Update
// ──────────────────────────────────────────────
function updateProgress() {
  const checks = document.querySelectorAll('.checklist-item input[type="checkbox"]');
  const checked = document.querySelectorAll('.checklist-item input[type="checkbox"]:checked');
  const total = checks.length;
  const done = checked.length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  const progressFill = document.querySelector('.checklist-progress-fill');
  const progressText = document.querySelector('.checklist-progress-text');
  const doneCount = document.querySelector('.checklist-done-count');

  if (progressFill) progressFill.style.width = `${pct}%`;
  if (progressText) progressText.textContent = `${pct}%`;
  if (doneCount) doneCount.textContent = `${done} / ${total}`;
}

// ──────────────────────────────────────────────
// Init Checklist
// ──────────────────────────────────────────────
function initChecklist() {
  const items = document.querySelectorAll('.checklist-item');
  if (!items.length) return;

  const state = loadState();

  items.forEach(item => {
    const checkbox = item.querySelector('input[type="checkbox"]');
    const id = checkbox?.id;
    if (!checkbox || !id) return;

    // Restore saved state
    if (state[id]) {
      checkbox.checked = true;
      item.classList.add('completed');
    }

    // Handle change
    checkbox.addEventListener('change', () => {
      const newState = loadState();
      if (checkbox.checked) {
        item.classList.add('completed');
        newState[id] = true;
      } else {
        item.classList.remove('completed');
        delete newState[id];
      }
      saveState(newState);
      updateProgress();
    });
  });

  updateProgress();
}

// ──────────────────────────────────────────────
// Filter by category
// ──────────────────────────────────────────────
function filterChecklist(category) {
  const items = document.querySelectorAll('.checklist-item');
  items.forEach(item => {
    if (category === 'all' || item.dataset.category === category) {
      item.style.display = '';
    } else {
      item.style.display = 'none';
    }
  });

  // Update active filter button
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.filter === category);
  });
}

// ──────────────────────────────────────────────
// Clear all
// ──────────────────────────────────────────────
function clearChecklist() {
  if (!confirm('Reset all checklist progress?')) return;
  saveState({});
  document.querySelectorAll('.checklist-item input[type="checkbox"]').forEach(cb => {
    cb.checked = false;
    cb.closest('.checklist-item')?.classList.remove('completed');
  });
  updateProgress();
  window.Toast && window.Toast.info('Checklist reset.');
}

// ──────────────────────────────────────────────
// Init
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initChecklist();

  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => filterChecklist(btn.dataset.filter || 'all'));
  });

  document.getElementById('btn-clear-checklist')?.addEventListener('click', clearChecklist);
});
