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
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()


def validate_config() -> None:
    if not BOT_TOKEN:
        raise SystemExit(
            "BOT_TOKEN не задан. Скопируй .env.example → .env и вставь токен от BotFather."
        )
    if not ACCESS_CODE:
        raise SystemExit("ACCESS_CODE не задан в .env")
    if not PDF_DIR.is_dir():
        raise SystemExit(f"Папка PDF не найдена: {PDF_DIR}")
