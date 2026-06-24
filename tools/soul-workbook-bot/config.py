# -*- coding: utf-8 -*-
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ACCESS_CODE = os.getenv("ACCESS_CODE", "SOUL-KATI-2026").strip().upper()

def _default_pdf_dir() -> Path:
    bundled = Path(__file__).resolve().parent / "pdfs"
    if bundled.is_dir() and any(bundled.glob("Soul-Method-Workbook-CHS*-tripwire-15eur.pdf")):
        return bundled
    return Path(__file__).resolve().parents[2] / "design" / "delivery"


# Папка с PDF (9 файлов CHS1–CHS9)
PDF_DIR = Path(os.getenv("PDF_DIR", str(_default_pdf_dir()))).resolve()
DATA_DIR = Path(os.getenv("DATA_DIR", str(Path(__file__).resolve().parent / "data"))).resolve()

MAX_CODE_ATTEMPTS = int(os.getenv("MAX_CODE_ATTEMPTS", "5"))
PORT = int(os.getenv("PORT", "8080"))
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook").strip() or "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").strip().rstrip("/")
if not WEBHOOK_URL and os.getenv("RENDER"):
    WEBHOOK_URL = "https://soul-method-workbook-bot.onrender.com"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()


def telegram_webhook_secret(raw: str) -> str | None:
    """Telegram allows only A-Z, a-z, 0-9, _, - in webhook secret_token."""
    import re

    cleaned = re.sub(r"[^A-Za-z0-9_-]", "", raw.strip())
    if 1 <= len(cleaned) <= 256:
        return cleaned
    return None


WEBHOOK_SECRET_SAFE = telegram_webhook_secret(WEBHOOK_SECRET)


def validate_config() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN не задан. Скопируй .env.example → .env и вставь токен от BotFather."
        )
    if not ACCESS_CODE:
        raise SystemExit("ACCESS_CODE не задан в .env")
    if not PDF_DIR.is_dir():
        raise SystemExit(f"Папка PDF не найдена: {PDF_DIR}")
