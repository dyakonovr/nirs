function accordionOpen(e) {
  const control = e.currentTarget;
  const self = control.parentElement;
  const content = self.querySelector('.accordion__content');

  self.classList.toggle('open');

  if (self.classList.contains('open')) {
    control.setAttribute('aria-expanded', true);
    content.setAttribute('aria-hidden', false);
    content.style.maxHeight = content.scrollHeight + 'px';
  } else {
    control.setAttribute('aria-expanded', false);
    content.setAttribute('aria-hidden', true);
    content.style.maxHeight = null;
  }
}