/* ============================================================
   progress.js — SVG progress ring utilities (reusable)
   ============================================================ */

'use strict';

/**
 * Animate all progress rings on the page.
 * Rings need: data-score attribute and .progress-ring-fill class.
 */
function initProgressRings() {
  document.querySelectorAll('.progress-ring').forEach(ring => {
    const fill = ring.querySelector('.progress-ring-fill');
    if (!fill) return;

    const score = parseInt(ring.dataset.score || '0', 10);
    const r = parseFloat(fill.getAttribute('r') || '54');
    const circumference = 2 * Math.PI * r;

    fill.style.strokeDasharray = circumference;
    fill.style.strokeDashoffset = circumference;

    // Set color based on score
    if (score >= 80)      fill.style.stroke = 'var(--status-secure)';
    else if (score >= 60) fill.style.stroke = 'var(--status-warning)';
    else                  fill.style.stroke = 'var(--status-danger)';

    const offset = circumference - (score / 100) * circumference;

    setTimeout(() => {
      fill.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1)';
      fill.style.strokeDashoffset = offset;
    }, 200);
  });
}

/**
 * Create a mini progress ring element programmatically.
 * @param {number} score 0-100
 * @param {number} size  diameter in px
 * @returns {SVGElement}
 */
function createMiniRing(score, size = 48) {
  const r = (size / 2) - 4;
  const c = 2 * Math.PI * r;
  const offset = c - (score / 100) * c;

  const color = score >= 80 ? 'var(--status-secure)' :
                score >= 60 ? 'var(--status-warning)' :
                              'var(--status-danger)';

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', size);
  svg.setAttribute('height', size);
  svg.setAttribute('viewBox', `0 0 ${size} ${size}`);

  const bgCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  bgCircle.setAttribute('cx', size / 2);
  bgCircle.setAttribute('cy', size / 2);
  bgCircle.setAttribute('r', r);
  bgCircle.setAttribute('fill', 'none');
  bgCircle.setAttribute('stroke', 'rgba(255,255,255,0.06)');
  bgCircle.setAttribute('stroke-width', '4');

  const fgCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  fgCircle.setAttribute('cx', size / 2);
  fgCircle.setAttribute('cy', size / 2);
  fgCircle.setAttribute('r', r);
  fgCircle.setAttribute('fill', 'none');
  fgCircle.setAttribute('stroke', color);
  fgCircle.setAttribute('stroke-width', '4');
  fgCircle.setAttribute('stroke-linecap', 'round');
  fgCircle.style.strokeDasharray = c;
  fgCircle.style.strokeDashoffset = c;
  fgCircle.style.transform = 'rotate(-90deg)';
  fgCircle.style.transformOrigin = 'center';
  fgCircle.style.transition = 'stroke-dashoffset 1s ease';

  svg.appendChild(bgCircle);
  svg.appendChild(fgCircle);

  // Animate
  requestAnimationFrame(() => {
    setTimeout(() => { fgCircle.style.strokeDashoffset = offset; }, 100);
  });

  return svg;
}

document.addEventListener('DOMContentLoaded', initProgressRings);
window.initProgressRings = initProgressRings;
window.createMiniRing = createMiniRing;
