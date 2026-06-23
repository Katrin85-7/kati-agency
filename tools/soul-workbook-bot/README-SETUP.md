# Soul Method · Telegram-бот выдачи воркбука

**Один код доступа** · **один PDF на Telegram-аккаунт** · **9 воркбуков по дате рождения**

Папка: `tools/soul-workbook-bot/`

---

## Что делает бот

1. `/start` → просит дату рождения  
2. Показывает архетип (CHS 1–9) → **Да / Исправить**  
3. Просит **код доступа** (ты отправляешь вручную после оплаты €15)  
4. Отправляет нужный PDF (~5 MB)  
5. Повторно тот же Telegram-аккаунт PDF не получит  

---

## Шаг 1 · Создать бота (бесплатно)

1. Telegram → [@BotFather](https://t.me/BotFather)  
2. `/newbot` → имя, например: `Soul Method Workbook`  
3. Username, например: `SoulMethodWorkbookBot`  
4. Скопируй **токен** (`123456:ABC...`)

---

## Шаг 2 · Настройка

```powershell
cd C:\Users\user\Desktop\CURSOR\tools\soul-workbook-bot
copy .env.example .env
```

Открой `.env`:

| Переменная | Значение |
|------------|----------|
| `BOT_TOKEN` | токен от BotFather |
| `ACCESS_CODE` | твой код, напр. `SOUL-KATI-2026` |

PDF должны лежать в `C:\Users\user\Desktop\CURSOR\design\delivery\`  
(`Soul-Method-Workbook-CHS1-tripwire-15eur.pdf` … `CHS9`).

---

## Шаг 3 · Запуск (тест, бесплатно)

Дважды кликни **`START-WORKBOOK-BOT.bat`**  
или:

```powershell
cd C:\Users\user\Desktop\CURSOR\tools\soul-workbook-bot
pip install -r requirements.txt
python bot.py
```

Окно должно оставаться открытым — пока ПК включён и скрипт работает, бот отвечает.

Проверь сама: открой бота → `/start` → дата → код → PDF.

---

## Что писать клиенту после оплаты

> Спасибо за оплату 🌿  
> 1. Открой бота: @ТвойBotUsername  
> 2. Нажми Start  
> 3. Введи дату рождения  
> 4. Код доступа: **SOUL-KATI-2026** (твой код из `.env`)  
> Воркбук придёт в чат — сохрани файл.

---

## База выдач

Файл `data/redemptions.db` — кто уже получил PDF (telegram_id, дата, CHS).  
Не удаляй, если не хочешь повторных выдач.

---

## Команды бота

| Команда | Действие |
|---------|----------|
| `/start` | Начать (или сообщение «уже получила») |
| `/cancel` | Сбросить текущий шаг |

---

## Позже (когда захочешь 24/7)

**Без карты (сейчас):** **`DEPLOY-RENDER.md`** · **`DEPLOY-RENDER.bat`** — Render free · $0

**С картой (стабильнее):** **`DEPLOY-24-7.md`** · **`DEPLOY-24-7.bat`** — Fly.io

Локально (только пока ПК включён): **`START-WORKBOOK-BOT.bat`**

---

## Агенты

| Задача | Кто |
|--------|-----|
| Логика бота, PDF | **Вебa** |
| Тексты в боте | **Ася** / Катрин |
| Публикация, ссылка в канале | **Тёя** |

*KATI Agency · июнь 2026*
