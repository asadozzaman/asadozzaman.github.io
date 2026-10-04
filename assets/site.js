'use strict';
const menu = document.querySelector('[data-menu]');
const nav = document.querySelector('#site-nav');
if (menu && nav) {
  menu.hidden = false;
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) { menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); }
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      menu.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); menu.focus();
    }
  });
}
const filters = document.querySelector('[data-filters]');
if (filters) {
  filters.hidden = false;
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    filters.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    document.querySelectorAll('[data-category]').forEach(card => {
      card.hidden = button.dataset.filter !== 'all' && button.dataset.filter !== card.dataset.category;
      if (!card.hidden) count++;
    });
    document.querySelector('[data-filter-status]').textContent = `${count} projects shown`;
  });
}
document.querySelectorAll('[data-explorer]').forEach(explorer => {
  explorer.querySelector('[data-explorer-controls]').hidden = false;
  let frame = '010';
  let mode = 'evidence';
  explorer.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.frame) {
      frame = button.dataset.frame;
      explorer.querySelectorAll('[data-frame]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    } else if (button.dataset.mode) {
      mode = button.dataset.mode;
      explorer.querySelectorAll('[data-mode]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    } else return;
    const image = explorer.querySelector('img');
    image.src = `${explorer.dataset.assetBase}${mode}_frame_${frame}.jpg`;
    image.alt = `${mode === 'evidence' ? 'Re-imported CVAT annotation over' : 'Unannotated'} synthetic source frame ${Number(frame)}`;
    explorer.querySelector('[data-frame-status]').textContent = `Frame ${Number(frame)} · ${mode === 'evidence' ? 're-imported annotation' : 'source video'}`;
  });
});
