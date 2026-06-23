# -*- coding: utf-8 -*-
"""Число сознания по дню рождения (Soul Method)."""
from __future__ import annotations

import re
from datetime import date, datetime

CHS_DAYS: dict[int, list[int]] = {
    1: [1, 10, 19, 28],
    2: [2, 11, 20, 29],
    3: [3, 12, 21, 30],
    4: [4, 13, 22, 31],
    5: [5, 14, 23],
    6: [6, 15, 24],
    7: [7, 16, 25],
    8: [8, 17, 26],
    9: [9, 18, 27],
}

ARCHETYPES: dict[int, str] = {
    1: "ЛИДЕР",
    2: "ДИПЛОМАТ",
    3: "ТВОРЕЦ",
    4: "АРХИТЕКТОР",
    5: "ИССЛЕДОВАТЕЛЬ",
    6: "НАСТАВНИК",
    7: "МУДРЕЦ",
    8: "УПРАВЛЕНЕЦ",
    9: "ГУМАНИСТ",
}

DATE_PATTERN = re.compile(
    r"^\s*(\d{1,2})[./\-](\d{1,2})[./\-](\d{4})\s*$"
)

MIN_BIRTH_YEAR = 1920
MAX_BIRTH_YEAR = date.today().year


def day_to_chs(day: int) -> int | None:
    for chs, days in CHS_DAYS.items():
        if day in days:
            return chs
    return None


def parse_birth_date(text: str) -> date | None:
    match = DATE_PATTERN.match(text.strip())
    if not match:
        return None
    d, m, y = (int(match.group(i)) for i in range(1, 4))
    if y < MIN_BIRTH_YEAR or y > MAX_BIRTH_YEAR:
        return None
    try:
        return date(y, m, d)
    except ValueError:
        return None


def format_birth_date_ru(d: date) -> str:
    months = (
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    )
    return f"{d.day} {months[d.month - 1]} {d.year}"


def pdf_filename(chs: int) -> str:
    return f"Soul-Method-Workbook-CHS{chs}-tripwire-15eur.pdf"
