// Мобільне меню
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mainNav = document.querySelector('.main-nav');

    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function() {
            mainNav.classList.toggle('menu-open');
        });
    }

    // Плавна прокрутка для внутрішніх посилань
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Обробка форми
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Дякуємо за ваш запит! Ми зв\'яжемося з вами найближчим часом.');
            contactForm.reset();
        });
    }

    // Активне посилання в навігації при прокрутці
    window.addEventListener('scroll', function() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - 100)) {
                current = section.getAttribute('id');
            }
        });

        const isDocumentsPage = window.location.pathname.endsWith('documents.html');
        document.querySelectorAll('.main-nav a').forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href') || '';
            if (href === `#${current}`) {
                link.classList.add('active');
            } else if (!current && (href === 'index.html' || href === '/' || href.endsWith('/index.html'))) {
                link.classList.add('active');
            } else if (isDocumentsPage && (href === 'documents.html' || href.endsWith('/documents.html'))) {
                link.classList.add('active');
            }
        });
    });
});
