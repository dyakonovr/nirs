const header = document.querySelector('#header');
const headerLogo = document.querySelector('#h-logo');
const headersLinks = document.querySelectorAll('#h-link');

window.addEventListener('scroll', function () {
  const scrollY = window.scrollY || document.documentElement.scrollTop;
  if (scrollY < 20) {
    header.className = "py-4 position-fixed top-0 bg-white"; 
    headerLogo.className = 'text-decoration-none link-info fs-2';
    headersLinks.forEach((link, idx) => {
      if (idx === 0) link.className = "ms-auto text-decoration-none link-primary";
      else link.className = "ms-3 text-decoration-none link-primary"
    });
  } else {
    header.className = "py-4 position-fixed top-0 bg-info"; 
    headerLogo.className = 'text-decoration-none link-light fs-2';
    headersLinks.forEach((link, idx) => {
      if (idx === 0) link.className = "ms-auto text-decoration-none link-light";
      else link.className = "ms-3 text-decoration-none link-light"
    });
  }
});