// Scroll reveal
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.07 });

document.querySelectorAll('.glass-card, .pipe-step, .sol-point').forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = `opacity .6s ease ${i * 0.05}s, transform .6s ease ${i * 0.05}s`;
  observer.observe(el);
});
