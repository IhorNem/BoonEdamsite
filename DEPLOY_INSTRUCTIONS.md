# ІНСТРУКЦІЯ ПО РОЗГОРТАННЮ САЙТУ

## Крок 1: Підготовка файлів

Всі файли знаходяться в папці `parkan-revolving-doors/`

Структура:
```
parkan-revolving-doors/
├── index.html
├── README.md
├── DEPLOY_INSTRUCTIONS.md
├── css/
│   ├── style.css
│   └── product.css
├── js/
│   └── script.js
├── images/
│   └── placeholder.jpg
└── products/
    ├── tqa.html
    ├── tournex.html
    ├── duotour.html
    ├── boonassist-tq.html
    ├── tqm.html
    ├── crystal-tq.html
    ├── tourlock-180.html
    ├── tourlock-120a.html
    └── tourlock-120s.html
```

## Крок 2: Завантаження на сервер

### Варіант A: FTP/SFTP
1. Підключіться до вашого сервера через FTP/SFTP клієнт (FileZilla, WinSCP)
2. Завантажте всю папку `parkan-revolving-doors` на сервер
3. Розмістіть файли у кореневій директорії веб-сайту (зазвичай `/public_html/` або `/www/`)

### Варіант B: cPanel File Manager
1. Увійдіть в cPanel
2. Відкрийте File Manager
3. Перейдіть до `/public_html/`
4. Завантажте всі файли через Upload
5. Розпакуйте архів (якщо завантажували архівом)

### Варіант C: SSH/Terminal
```bash
# Підключення до сервера
ssh user@your-server.com

# Перехід до директорії сайту
cd /var/www/html/

# Завантаження файлів (якщо є доступ через scp)
scp -r /path/to/parkan-revolving-doors/* user@server:/var/www/html/
```

## Крок 3: Додавання зображень продукції

### Необхідні зображення:
Розмістіть зображення у папці `images/`:

**Для карток продуктів (400x300px):**
- tqa.jpg
- tournex.jpg
- duotour.jpg
- boonassist-tq.jpg
- tqm.jpg
- crystal-tq.jpg
- tourlock-180.jpg
- tourlock-120a.jpg
- tourlock-120s.jpg

**Для сторінок продуктів (800x600px):**
- tqa-large.jpg
- tournex-large.jpg
- duotour-large.jpg
- boonassist-large.jpg
- tqm-large.jpg
- crystal-large.jpg
- tourlock180-large.jpg
- tourlock120a-large.jpg
- tourlock120s-large.jpg

### Оптимізація зображень:
- Використовуйте JPG для фотографій
- Якість: 80-85%
- Інструменти: TinyPNG, ImageOptim, або онлайн-сервіси

## Крок 4: Налаштування форми зворотного зв'язку

Форма на сайті потребує серверної обробки. Є два варіанти:

### Варіант A: PHP обробник (рекомендовано)
Створіть файл `send-form.php`:

```php
<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']);
    $phone = htmlspecialchars($_POST['phone']);
    $email = htmlspecialchars($_POST['email']);
    $message = htmlspecialchars($_POST['message']);
    
    $to = "info@parkan.ua";
    $subject = "Новий запит з сайту Parkan.ua";
    $body = "Ім'я: $name\nТелефон: $phone\nEmail: $email\nПовідомлення: $message";
    $headers = "From: noreply@parkan.ua";
    
    if (mail($to, $subject, $body, $headers)) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false]);
    }
}
?>
```

Змініть у файлі `js/script.js` обробку форми:
```javascript
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(contactForm);
    
    fetch('send-form.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Дякуємо за ваш запит! Ми зв\'яжемося з вами найближчим часом.');
            contactForm.reset();
        }
    });
});
```

### Варіант B: Використання сторонніх сервісів
- Formspree.io
- EmailJS
- Google Forms

## Крок 5: Налаштування .htaccess (опціонально)

Створіть файл `.htaccess` для покращення SEO:

```apache
# Увімкнення перезапису URL
RewriteEngine On

# Видалення .html з URL
RewriteCond %{REQUEST_FILENAME} !-d
RewriteCond %{REQUEST_FILENAME}.html -f
RewriteRule ^(.*)$ $1.html [L]

# HTTPS редирект (якщо є SSL)
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Кешування файлів
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access 1 year"
    ExpiresByType image/jpeg "access 1 year"
    ExpiresByType image/png "access 1 year"
    ExpiresByType text/css "access 1 month"
    ExpiresByType application/javascript "access 1 month"
</IfModule>

# Стиснення файлів
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>
```

## Крок 6: Перевірка роботи сайту

1. Відкрийте сайт у браузері: `https://yourdomain.com`
2. Перевірте всі сторінки продуктів
3. Протестуйте форму зворотного зв'язку
4. Перевірте адаптивність на мобільних пристроях
5. Перевірте швидкість завантаження (Google PageSpeed Insights)

## Крок 7: SEO налаштування

### Google Search Console
1. Додайте сайт у Google Search Console
2. Завантажте sitemap.xml (створіть його)
3. Перевірте індексацію сторінок

### Sitemap.xml
Створіть файл `sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yourdomain.com/products/tqa.html</loc>
    <priority>0.8</priority>
  </url>
  <!-- Додайте інші сторінки -->
</urlset>
```

### Google Analytics (опціонально)
Додайте код відстеження перед закриваючим тегом `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## Крок 8: Безпека

1. Оновлюйте систему керування контентом (якщо використовується)
2. Використовуйте HTTPS (SSL сертифікат)
3. Регулярно робіть резервні копії
4. Захистіть адміністративні файли

## Підтримка та оновлення

### Регулярні завдання:
- Перевірка працездатності форми
- Оновлення контактної інформації
- Додавання нових продуктів (за потреби)
- Моніторинг трафіку через Google Analytics

### Контакти для питань:
Email: info@parkan.ua
Телефон: +38 (067) 630-13-24

## Додаткові рекомендації

1. **Продуктивність:**
   - Оптимізуйте зображення перед завантаженням
   - Використовуйте CDN для статичних файлів
   - Увімкніть кешування на сервері

2. **Мобільна версія:**
   - Перевірте на різних пристроях
   - Використовуйте Chrome DevTools для тестування

3. **Доступність:**
   - Додайте alt-тексти до всіх зображень
   - Перевірте контрастність кольорів
   - Забезпечте навігацію з клавіатури

## Підтримка браузерів

Сайт підтримує:
- Chrome (останні 2 версії)
- Firefox (останні 2 версії)
- Safari (останні 2 версії)
- Edge (останні 2 версії)
- Мобільні браузери iOS і Android

---

**Успішного розгортання!**

Якщо виникнуть питання, зверніться до розробників або до команди підтримки Parkan.ua.
