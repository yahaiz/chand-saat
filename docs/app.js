// Interactive Desktop Simulator Tab Navigation & FAQ Accordion
document.addEventListener('DOMContentLoaded', () => {
  // Tab Switcher for Desktop Simulator Demo
  const menuButtons = document.querySelectorAll('.nav-item[data-target]');
  const viewPanes = document.querySelectorAll('.view-panel');

  menuButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetViewId = btn.getAttribute('data-target');
      if (!targetViewId) return;

      // Update Active Menu State
      menuButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Update View Pane
      viewPanes.forEach(pane => {
        pane.classList.remove('active');
        pane.style.display = 'none';
        if (pane.id === `view-${targetViewId}`) {
          pane.classList.add('active');
          pane.style.display = 'block';
        }
      });
    });
  });

  // FAQ Accordion Handler
  const faqItems = document.querySelectorAll('.faq-item-card');

  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question-btn');
    if (!questionBtn) return;

    questionBtn.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close all FAQs
      faqItems.forEach(i => {
        i.classList.remove('open');
        const icon = i.querySelector('.faq-icon');
        if (icon) icon.textContent = '+';
      });

      // Toggle current if was not open
      if (!isOpen) {
        item.classList.add('open');
        const icon = item.querySelector('.faq-icon');
        if (icon) icon.textContent = '−';
      }
    });
  });
});
