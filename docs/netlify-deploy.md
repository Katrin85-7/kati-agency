# Деплой Kati Agency на Netlify

Сайт — **статический HTML** без сборки. Netlify отдаёт `index.html` и папку `assets/` как есть.

## Что уже в репозитории

| Файл | Зачем |
|------|--------|
| `netlify.toml` | Настройки публикации, кэш, заголовки безопасности |
| `404.html` | Редирект на главную при ошибочных URL |
| `.github/workflows/deploy-pages.yml` | GitHub Pages (можно оставить параллельно) |

## Быстрый старт (5 минут)

### 1. Закоммить и запушить файлы деплоя

Если `netlify.toml` ещё не в GitHub:

```powershell
cd "C:\Users\user\Desktop\CURSOR\Kati-Agency\kati-agency-site"
git add netlify.toml 404.html docs/netlify-deploy.md README.md
git commit -m "Add Netlify deploy config and guide."
git push origin main
```

### 2. Подключить репозиторий в Netlify

1. Зайди на [app.netlify.com](https://app.netlify.com) → **Add new site** → **Import an existing project**
2. **GitHub** → репозиторий **`Katrin85-7/kati-agency`**
3. Netlify подхватит `netlify.toml` автоматически. Если спросит вручную:

| Поле | Значение |
|------|----------|
| **Branch to deploy** | `main` |
| **Build command** | *(пусто)* |
| **Publish directory** | `.` |

4. **Deploy site**

Через 1–2 минуты появится URL вида `https://random-name-123.netlify.app`.

### 3. Переименовать сайт (опционально)

**Site configuration → Domain management → Options → Edit site name**

Пример: **`katrin-kati-agency`** → **https://katrin-kati-agency.netlify.app**

> Не используй имя `kati-agency` — адрес `kati-agency.netlify.app` уже занят другим сайтом.

---

## Свой домен

1. **Domain management → Add a domain** → введи домен (например `katiagency.com`)
2. Netlify покажет DNS-записи. Обычно:
   - **A** `@` → `75.2.60.5`
   - **CNAME** `www` → `your-site.netlify.app`
3. Включи **HTTPS** (Let's Encrypt) — Netlify делает это автоматически после проверки DNS.

---

## Чеклист после деплоя

Открой сайт **на телефоне** и проверь:

- [ ] Первый экран: фото, видео, текст читается
- [ ] Бургер-меню и якоря (Подход, SOUL, Услуги, FAQ…)
- [ ] Карусель кейсов: аватары, До/После, стрелки
- [ ] Кнопки «Записаться» → копирование текста + Instagram
- [ ] «Начать путь» → блок **Услуги**

---

## Обновление сайта

Любой `git push` в `main` → Netlify пересобирает и публикует автоматически (если включён auto deploy).

---

## Переменные окружения

Для текущей версии **не нужны**. Если позже добавишь формы Netlify Forms или аналитику — переменные задаются в **Site configuration → Environment variables**.

---

## Drag & drop (без Git)

Если нужно выложить разово без GitHub:

1. [app.netlify.com/drop](https://app.netlify.com/drop)
2. Перетащи папку проекта (с `index.html` и `assets/` в корне)

Для постоянных обновлений удобнее связка **GitHub + Netlify**.

---

## GitHub Pages vs Netlify

| | GitHub Pages | Netlify |
|---|--------------|---------|
| URL сейчас | katrin85-7.github.io/kati-agency | свой `.netlify.app` или домен |
| Сборка | GitHub Actions | `netlify.toml`, без сборки |
| Домен | через DNS | встроенный мастер |
| Формы | нет | Netlify Forms (если понадобится) |

Оба хостинга могут работать параллельно. Для продакшена обычно выбирают один основной URL и настраивают редирект.

---

## Если деплой падает с ошибкой

### «Deploy directory 'dist' / 'build' / 'public' does not exist»

Netlify ищет папку сборки, которой у нас **нет** — сайт статический.

**Site configuration → Build & deploy → Continuous deployment → Build settings:**

| Поле | Правильно | Неправильно |
|------|-----------|-------------|
| **Base directory** | *(пусто)* | `kati-agency-site`, `src`… |
| **Build command** | *(пусто)* или `echo Static site` | `npm run build` |
| **Publish directory** | `.` | `dist`, `build`, `public` |

Нажми **Save**, затем **Deploys → Trigger deploy → Clear cache and deploy site**.

---

### «Build script returned non-zero exit code»

Чаще всего в Build command случайно стоит `npm run build`, а `package.json` в проекте нет.

Очисти Build command (оставь пустым) или поставь: `echo Static site`

---

### Сайт открылся, но это НЕ твой лендинг

URL **`https://kati-agency.netlify.app`** сейчас показывает **чужой старый сайт** (интернет-маркетинг), не репозиторий [Katrin85-7/kati-agency](https://github.com/Katrin85-7/kati-agency).

**Что делать:**

1. Зайди в [app.netlify.com](https://app.netlify.com) → свой сайт из списка (тот, что подключён к GitHub)
2. **Domain management → Options → Change site name** → уникальное имя, например:
   - `katrin-kati-agency`
   - `kati-agency-landing`
   - `kati-agency-2026`
3. Твой URL будет: `https://ИМЯ-САЙТА.netlify.app`

Проверка: на главной должны быть заголовок **«Создаём бренды, которые невозможно скопировать»** и кнопка **«Начать путь проявленности»**.

---

### «Page not found» после успешного деплоя

- **Publish directory** должен быть `.` (корень репо, где лежит `index.html`)
- **Base directory** — пустой
- В Deploy file browser должны быть `index.html` и папка `assets/` в корне

---

### Netlify не видит репозиторий GitHub

1. **User settings → Applications → GitHub** → дать Netlify доступ
2. При импорте выбрать **Katrin85-7/kati-agency**, ветка **main**
3. Если репо не в списке — **Configure Netlify on GitHub** для этого репо

---

### Быстрый запасной вариант (без Git)

1. [app.netlify.com/drop](https://app.netlify.com/drop)
2. Перетащи папку `kati-agency-site` целиком (внутри должны быть `index.html` + `assets/`)

---

## Если что-то не грузится

1. **Site deploys** — последний деплой зелёный?
2. **Deploy log** — нет ли ошибок пути publish
3. **Missing files** — в репозитории должны быть все файлы из `assets/`, на которые ссылается `index.html`:
   - `hero-horse.jpg`
   - `katrin-about.jpg`
   - `katrin-hero.jpg`
   - и остальные картинки в `assets/`

Если файла нет в Git — добавь, закоммить, push.

---

## Контакты в проекте (для проверки кнопок)

- Instagram Direct: `https://ig.me/m/katrina.zhur`
- Telegram: `https://t.me/Katrina_zhur`
