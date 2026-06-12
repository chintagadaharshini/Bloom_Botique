// ─────────────────────────────────────
// HAMBURGER MENU (Mobile)
// ─────────────────────────────────────
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.navbar-nav');

if (hamburger) {
  hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
  });
}

// ─────────────────────────────────────
// AUTO-DISMISS ALERTS after 4 seconds
// ─────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });
});