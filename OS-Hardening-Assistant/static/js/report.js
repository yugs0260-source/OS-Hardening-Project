/* ============================================================
   report.js — Report print and export functionality
   ============================================================ */

'use strict';

// ──────────────────────────────────────────────
// Print report
// ──────────────────────────────────────────────
function printReport() {
  window.print();
}

// ──────────────────────────────────────────────
// Export report as HTML file
// ──────────────────────────────────────────────
function exportReportHTML() {
  const reportEl = document.querySelector('.report-page');
  if (!reportEl) return;

  const styles = Array.from(document.querySelectorAll('link[rel="stylesheet"], style'))
    .map(el => el.outerHTML)
    .join('\n');

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OS Hardening Report — ${new Date().toLocaleDateString()}</title>
${styles}
<style>
  body { background: #fff !important; color: #1a1a1a !important; }
  .sidebar, .topbar, .print-actions { display: none !important; }
  .main-content { margin: 0 !important; padding: 20px !important; }
</style>
</head>
<body>
${reportEl.outerHTML}
</body>
</html>`;

  const blob = new Blob([html], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `security-report-${new Date().toISOString().slice(0, 10)}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  window.Toast && window.Toast.success('Report downloaded as HTML');
}

// ──────────────────────────────────────────────
// Copy report summary to clipboard
// ──────────────────────────────────────────────
function copyReportSummary() {
  const rows = document.querySelectorAll('.report-check-row');
  const lines = ['OS Hardening Assistant — Security Report', '='.repeat(50), ''];

  rows.forEach(row => {
    const title = row.querySelector('.report-check-title')?.textContent.trim();
    const status = row.querySelector('.badge')?.textContent.trim();
    const detail = row.querySelector('.report-check-detail')?.textContent.trim();
    const rec = row.querySelector('.report-check-rec')?.textContent.trim();
    if (title) {
      lines.push(`[${status}] ${title}`);
      if (detail) lines.push(`  Detail: ${detail}`);
      if (rec)    lines.push(`  Action: ${rec}`);
      lines.push('');
    }
  });

  const scoreEl = document.querySelector('.big-number');
  if (scoreEl) {
    lines.push(`Overall Score: ${scoreEl.textContent}/100`);
  }

  lines.push(`Generated: ${new Date().toLocaleString()}`);

  window.copyToClipboard && window.copyToClipboard(lines.join('\n'));
}

// ──────────────────────────────────────────────
// Init
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-print')?.addEventListener('click', printReport);
  document.getElementById('btn-export-html')?.addEventListener('click', exportReportHTML);
  document.getElementById('btn-copy-summary')?.addEventListener('click', copyReportSummary);
});

window.printReport = printReport;
window.exportReportHTML = exportReportHTML;
window.copyReportSummary = copyReportSummary;
