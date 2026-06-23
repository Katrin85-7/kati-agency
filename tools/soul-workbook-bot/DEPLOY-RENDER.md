# Soul Method bot · Render · $0 · без карты

Пока мало заказов — **Render free tier**. Карта **не нужна**.

---

## Что получишь

- Бот `@method_soulbot` работает **без твоего ПК**
- **$0** на free plan Render
- Минус free: сервис «засыпает» через 15 мин без трафика → решается **UptimeRobot** (бесплатно, без карты)

Fly.io с картой — когда заказов станет больше и захочешь стабильнее.

---

## Шаг 0 · Подготовка PDF (один раз)

```powershell
cd C:\Users\user\Desktop\CURSOR\tools\soul-workbook-bot
.\prepare-deploy.ps1
```

Скопирует 9 PDF в папку `pdfs/` — они нужны внутри Docker-образа.

---

## Шаг 1 · GitHub (если ещё нет репо)

1. [github.com/new](https://github.com/new) → репо, например `kati-cursor` (private)
2. В PowerShell:

```powershell
cd C:\Users\user\Desktop\CURSOR
git add tools/soul-workbook-bot
git commit -m "Soul Method workbook Telegram bot for Render"
git branch -M main
git remote add origin https://github.com/ТВОЙ_ЛОГИН/kati-cursor.git
git push -u origin main
```

> PDF ~48 MB — push может занять несколько минут. Это нормально.

---

## Шаг 2 · Render (без карты)

1. [render.com](https://render.com) → **Sign up with GitHub**
2. **New +** → **Blueprint**
3. Подключи репо → Render найдёт `tools/soul-workbook-bot/render.yaml`
4. При создании введи **`BOT_TOKEN`** (из `.env`, BotFather)
5. **Apply** → дождись **Live** (~5–10 мин, первая сборка Docker)

URL сервиса будет вида:  
`https://soul-method-workbook-bot.onrender.com`

Проверка: открой `/health` → должно быть `ok`.

---

## Шаг 3 · UptimeRobot (чтобы не засыпал)

1. [uptimerobot.com](https://uptimerobot.com) → бесплатный аккаунт
2. **Add monitor** → тип **HTTP(s)**
3. URL: `https://soul-method-workbook-bot.onrender.com/health`
4. Interval: **5 minutes**
5. Save

Без пинга бот может «проснуться» 30–60 сек после первого `/start`.

---

## Шаг 4 · Локальный бот — выключить

Закрой `START-WORKBOOK-BOT.bat`, если открыт.  
Telegram принимает **один** активный webhook/polling.

---

## Проверка

Telegram → `@method_soulbot` → `/start` → дата → код `SOUL-KATI-2026` → PDF.

---

## Сколько это стоит

| | Render free | Fly.io |
|---|-------------|--------|
| Карта | **не нужна** | нужна |
| Деньги | **$0** | ~$2–5/мес |
| Сон | да (15 мин) → UptimeRobot | нет |

---

## Если что-то не так

| Симптом | Решение |
|---------|---------|
| Build failed, нет PDF | `prepare-deploy.ps1` → commit `pdfs/` → push |
| Бот молчит | Render → Logs; проверь `BOT_TOKEN` |
| Долго отвечает | UptimeRobot на `/health` каждые 5 мин |
| Webhook error | Render → Environment → `WEBHOOK_URL` = `https://ИМЯ.onrender.com` (без `/webhook`) |

---

## Быстрый запуск

Дважды кликни **`DEPLOY-RENDER.bat`** — откроет чек-лист и нужные сайты.

*KATI Agency · июнь 2026*
