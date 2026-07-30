// Interactive Desktop Simulator Tab Navigation, FAQ Accordion, & GitHub Release Auto-Sync
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

  // Fetch Latest Release Version and Asset Links dynamically from GitHub Releases API
  async function syncLatestRelease() {
    try {
      const response = await fetch('https://api.github.com/repos/yahaiz/chand-saat/releases/latest');
      if (!response.ok) return;
      const data = await response.json();

      const tagName = data.tag_name; // e.g. "v0.2.1"
      const verClean = tagName.replace(/^v/, '');

      // Update Hero Version Badge
      const versionBadge = document.getElementById('version-badge');
      if (versionBadge) {
        versionBadge.textContent = `نسخه v${verClean} — ۱۰۰٪ رایگان و آفلاین`;
      }

      // Locate Asset URLs from API
      let setupUrl = `https://github.com/yahaiz/chand-saat/releases/download/${tagName}/ChandSaat_Setup_v${verClean}.exe`;
      let portableUrl = `https://github.com/yahaiz/chand-saat/releases/download/${tagName}/ChandSaat_v${verClean}_Portable.zip`;

      if (data.assets && Array.isArray(data.assets)) {
        const setupAsset = data.assets.find(a => a.name.includes('Setup') && a.name.endsWith('.exe'));
        const portableAsset = data.assets.find(a => a.name.includes('Portable') && a.name.endsWith('.zip'));

        if (setupAsset && setupAsset.browser_download_url) {
          setupUrl = setupAsset.browser_download_url;
        }
        if (portableAsset && portableAsset.browser_download_url) {
          portableUrl = portableAsset.browser_download_url;
        }
      }

      // Update all Setup download buttons
      document.querySelectorAll('.btn-dl-setup').forEach(el => {
        el.href = setupUrl;
      });

      // Update all Portable download buttons
      document.querySelectorAll('.btn-dl-portable').forEach(el => {
        el.href = portableUrl;
      });
    } catch (err) {
      console.log('GitHub Release sync info:', err);
    }
  }

  syncLatestRelease();
});
