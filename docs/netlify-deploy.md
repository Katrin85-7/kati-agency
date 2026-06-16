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

Пример: `kati-agency` → **https://kati-agency.netlify.app**

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
