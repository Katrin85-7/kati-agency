# Render Environment — сверь с Dashboard

Открой: soul-method-workbook-bot → Environment

Должно быть ТОЧНО так (кроме BOT_TOKEN — свой):

| Key | Value |
|-----|--------|
| BOT_TOKEN | из файла .env (не .env.example) |
| ACCESS_CODE | SOUL-KATI-2026 |
| WEBHOOK_URL | https://soul-method-workbook-bot.onrender.com |
| WEBHOOK_SECRET | SoulMethod-Kati-2026-wh |
| PDF_DIR | /app/pdfs |
| DATA_DIR | /data |
| PORT | 10000 |

После правок: Save Changes → Manual Deploy → Deploy latest commit

Blueprint: Manual sync (подтянет новый код с GitHub)
