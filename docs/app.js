/* ==========================================================================
   ChandSaat (چند ساعت؟) - Landing Page Interactive Logic & Audio Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // --------------------------------------------------------------------------
  // 1. App Window Simulator Tab Switcher
  // --------------------------------------------------------------------------
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const activePane = document.getElementById(`tab-${targetTab}`);
      if (activePane) {
        activePane.classList.add('active');
      }
    });
  });

  // --------------------------------------------------------------------------
  // 2. Interactive Study Progress Calculator
  // --------------------------------------------------------------------------
  const rangeDays = document.getElementById('range-days');
  const rangeHours = document.getElementById('range-hours');
  const rangeTests = document.getElementById('range-tests');

  const valDays = document.getElementById('val-days');
  const valHours = document.getElementById('val-hours');
  const valTests = document.getElementById('val-tests');

  const resTotalHours = document.getElementById('res-total-hours');
  const resTotalTests = document.getElementById('res-total-tests');
  const levelBadge = document.getElementById('level-badge');

  function calculateProgress() {
    if (!rangeDays || !rangeHours || !rangeTests) return;

    const days = parseInt(rangeDays.value);
    const hours = parseFloat(rangeHours.value);
    const tests = parseInt(rangeTests.value);

    valDays.textContent = `${days} روز`;
    valHours.textContent = `${hours} ساعت`;
    valTests.textContent = `${tests} تست`;

    const totalHours = Math.round(days * hours);
    const totalTests = Math.round(days * tests);

    resTotalHours.textContent = totalHours.toLocaleString('fa-IR');
    resTotalTests.textContent = totalTests.toLocaleString('fa-IR');

    // Determine Level Badge
    let badgeText = '🌱 شروع پرقدرت';
    let badgeColor = '#10b981';

    if (totalHours > 400 && totalTests > 5000) {
      badgeText = '👑 رتبه برتر کنکور (فوق‌العاده)';
      badgeColor = '#ec4899';
    } else if (totalHours > 200 && totalTests > 2500) {
      badgeText = '🔥 تسلط عالی و آمادگی بالا';
      badgeColor = '#f59e0b';
    } else if (totalHours > 80 && totalTests > 1000) {
      badgeText = '⚡ پیشرفت منظم و پایدار';
      badgeColor = '#06b6d4';
    }

    levelBadge.textContent = badgeText;
    levelBadge.style.borderColor = badgeColor;
    levelBadge.style.color = badgeColor;
  }

  if (rangeDays && rangeHours && rangeTests) {
    rangeDays.addEventListener('input', calculateProgress);
    rangeHours.addEventListener('input', calculateProgress);
    rangeTests.addEventListener('input', calculateProgress);
    calculateProgress();
  }

  // --------------------------------------------------------------------------
  // 3. Live Interactive Pomodoro Timer & Audio Engine
  // --------------------------------------------------------------------------
  let timerInterval = null;
  let timeLeft = 25 * 60; // 25 minutes in seconds
  let isTimerRunning = false;

  const timerDisplay = document.getElementById('sim-pomo-display');
  const pomoStatus = document.getElementById('sim-pomo-status');
  const btnStart = document.getElementById('pomo-start-btn');
  const btnReset = document.getElementById('pomo-reset-btn');

  function updateTimerDisplay() {
    if (!timerDisplay) return;
    const mins = Math.floor(timeLeft / 60).toString().padStart(2, '0');
    const secs = (timeLeft % 60).toString().padStart(2, '0');
    timerDisplay.textContent = `${mins}:${secs}`;
  }

  if (btnStart) {
    btnStart.addEventListener('click', () => {
      if (isTimerRunning) {
        // Pause
        clearInterval(timerInterval);
        isTimerRunning = false;
        btnStart.textContent = '▶️ ادامه پومودورو';
        pomoStatus.textContent = '⏸️ متوقف شده';
        pomoStatus.style.color = '#f59e0b';
      } else {
        // Start
        isTimerRunning = true;
        btnStart.textContent = '⏸️ توقف موقت';
        pomoStatus.textContent = '⏱️ جلسه مطالعه فعال است...';
        pomoStatus.style.color = '#10b981';

        timerInterval = setInterval(() => {
          if (timeLeft > 0) {
            timeLeft--;
            updateTimerDisplay();
          } else {
            clearInterval(timerInterval);
            isTimerRunning = false;
            btnStart.textContent = '▶️ شروع مجدد';
            pomoStatus.textContent = '🎉 زمان استراحت فرا رسید!';
            pomoStatus.style.color = '#ec4899';
            playChimeSound();
          }
        }, 1000);
      }
    });
  }

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      clearInterval(timerInterval);
      isTimerRunning = false;
      timeLeft = 25 * 60;
      updateTimerDisplay();
      if (btnStart) btnStart.textContent = '▶️ شروع پومودورو';
      if (pomoStatus) {
        pomoStatus.textContent = 'آماده برای جلسه ۲۵ دقیقه‌ای';
        pomoStatus.style.color = '#06b6d4';
      }
    });
  }

  // --------------------------------------------------------------------------
  // Web Audio Synth (White Noise & Completion Chime without external files)
  // --------------------------------------------------------------------------
  let audioCtx = null;
  let noiseNode = null;
  let isNoisePlaying = false;

  const btnAmbient = document.getElementById('ambient-sound-btn');

  function toggleAmbientSound() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (isNoisePlaying) {
      if (noiseNode) {
        noiseNode.stop();
        noiseNode.disconnect();
      }
      isNoisePlaying = false;
      if (btnAmbient) {
        btnAmbient.classList.remove('active');
        btnAmbient.innerHTML = '🌧️ پخش نویز سفید / صدای باران';
      }
    } else {
      // Create Pink/Brown Ambient Noise
      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;

      for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        b0 = 0.99886 * b0 + white * 0.0555179;
        b1 = 0.99332 * b1 + white * 0.0750759;
        b2 = 0.96900 * b2 + white * 0.1538520;
        b3 = 0.86650 * b3 + white * 0.3104856;
        b4 = 0.55000 * b4 + white * 0.5329522;
        b5 = -0.7616 * b5 - white * 0.0168980;
        output[i] = b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362;
        output[i] *= 0.02; // Keep volume soft
        b6 = white * 0.115926;
      }

      noiseNode = audioCtx.createBufferSource();
      noiseNode.buffer = noiseBuffer;
      noiseNode.loop = true;
      
      const gainNode = audioCtx.createGain();
      gainNode.gain.value = 0.2;
      
      noiseNode.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      
      noiseNode.start();
      isNoisePlaying = true;

      if (btnAmbient) {
        btnAmbient.classList.add('active');
        btnAmbient.innerHTML = '🔊 توقف صدای باران (در حال پخش)';
      }
    }
  }

  function playChimeSound() {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5 note
      osc.frequency.exponentialRampToValueAtTime(1046.5, ctx.currentTime + 0.8);

      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.8);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start();
      osc.stop(ctx.currentTime + 0.8);
    } catch (e) {
      console.log('Audio chime not supported or muted.');
    }
  }

  if (btnAmbient) {
    btnAmbient.addEventListener('click', toggleAmbientSound);
  }

  // --------------------------------------------------------------------------
  // 4. FAQ Accordion Logic
  // --------------------------------------------------------------------------
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      faqItems.forEach(i => i.classList.remove('active'));
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });

  // --------------------------------------------------------------------------
  // 5. Fetch Latest Release Version from GitHub API
  // --------------------------------------------------------------------------
  async function fetchLatestRelease() {
    try {
      const response = await fetch('https://api.github.com/repos/yahaiz/chand-saat/releases/latest');
      if (response.ok) {
        const data = await response.json();
        const versionTag = data.tag_name || 'v0.2.0';
        
        const badgeElem = document.getElementById('latest-version-badge');
        if (badgeElem) {
          badgeElem.textContent = `نسخه نهایی ${versionTag}`;
        }
      }
    } catch (err) {
      console.log('GitHub API offline or rate-limited, using fallback version.');
    }
  }

  fetchLatestRelease();
});
