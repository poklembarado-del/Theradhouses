/* Radhouses — site behaviour. No dependencies. */
(function () {
  'use strict';

  /* ---------- theme toggle ---------- */
  var root = document.documentElement;
  var STORE = 'radhouses-theme';

  function systemDark() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function currentTheme() {
    return root.getAttribute('data-theme') || (systemDark() ? 'dark' : 'light');
  }
  function applyTheme(t) {
    root.setAttribute('data-theme', t);
    var btn = document.querySelector('.theme-toggle');
    if (btn) {
      btn.textContent = t === 'dark' ? '☀' : '☾';
      btn.setAttribute('aria-label', btn.dataset[t === 'dark' ? 'labelLight' : 'labelDark'] || 'Toggle theme');
    }
  }

  try {
    var saved = localStorage.getItem(STORE);
    if (saved) { applyTheme(saved); }
  } catch (e) { /* storage unavailable — fall back to system preference */ }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.theme-toggle');
    if (!btn) return;
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    try { localStorage.setItem(STORE, next); } catch (err) {}
  });

  /* set the initial icon even when no preference is stored */
  applyTheme(currentTheme());

  /* ---------- mobile navigation ---------- */
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.textContent = open ? '✕' : '☰';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = '☰';
      }
    });
  }

  /* ---------- rental ROI calculator ---------- */
  var calc = document.getElementById('roi');
  if (!calc) return;

  var locale = document.documentElement.lang === 'sk' ? 'sk-SK' : 'en-IE';
  var money = new Intl.NumberFormat(locale, {
    style: 'currency', currency: 'EUR', maximumFractionDigits: 0
  });

  var inputs = {
    price:     document.getElementById('c-price'),
    rate:      document.getElementById('c-rate'),
    occupancy: document.getElementById('c-occ'),
    costs:     document.getElementById('c-cost')
  };

  var out = {
    price:   document.getElementById('o-price'),
    rate:    document.getElementById('o-rate'),
    occ:     document.getElementById('o-occ'),
    cost:    document.getElementById('o-cost'),
    nights:  document.getElementById('r-nights'),
    gross:   document.getElementById('r-gross'),
    running: document.getElementById('r-running'),
    net:     document.getElementById('r-net'),
    payback: document.getElementById('r-payback'),
    yield:   document.getElementById('r-yield')
  };

  var paybackUnit = calc.dataset.years || 'years';

  function recalc() {
    var price = +inputs.price.value;
    var rate  = +inputs.rate.value;
    var occ   = +inputs.occupancy.value;
    var cost  = +inputs.costs.value;

    var nights  = Math.round(365 * occ / 100);
    var gross   = nights * rate;
    var running = gross * cost / 100;
    var net     = gross - running;
    var payback = net > 0 ? price / net : Infinity;
    var yieldPc = price > 0 ? (net / price) * 100 : 0;

    out.price.value = money.format(price);
    out.rate.value  = money.format(rate);
    out.occ.value   = occ + ' %';
    out.cost.value  = cost + ' %';

    out.nights.textContent  = nights;
    out.gross.textContent   = money.format(gross);
    out.running.textContent = '−' + money.format(running);
    out.net.textContent     = money.format(net);
    out.yield.textContent   = yieldPc.toFixed(1) + ' %';
    out.payback.textContent = isFinite(payback)
      ? payback.toFixed(1) + ' ' + paybackUnit
      : '—';
  }

  Object.keys(inputs).forEach(function (k) {
    inputs[k].addEventListener('input', recalc);
  });
  recalc();
})();
