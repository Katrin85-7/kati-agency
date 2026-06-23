# -*- coding: utf-8 -*-
"""Исправляет padding обложки в print CSS и page height во всех 9 HTML файлах."""
from pathlib import Path

DESIGN = Path(r"C:\Users\user\Desktop\CURSOR\design")

HTML_FILES = [
    DESIGN / "workbook-tripwire-raspakovka.html",
    DESIGN / "workbook-tripwire-CHS2-DIPLOMAT.html",
    DESIGN / "workbook-tripwire-CHS3-TVOREC.html",
    DESIGN / "workbook-tripwire-CHS4-ARHITEKTOR.html",
    DESIGN / "workbook-tripwire-CHS5-ISSLEDOVATEL.html",
    DESIGN / "workbook-tripwire-CHS6-NASTAVNIK.html",
    DESIGN / "workbook-tripwire-CHS7-MUDREC.html",
    DESIGN / "workbook-tripwire-CHS8-UPRAVLENEC.html",
    DESIGN / "workbook-tripwire-CHS9-GUMANNIST.html",
]

FIXES = [
    # 1. print CSS: убираем padding у обложки и фиксируем размер
    (
        ".page--cover { padding: 12mm 16mm 10mm !important; }",
        ".page--cover { padding: 0 !important; height: 297mm !important; overflow: hidden !important; }"
    ),
    # 2. cover-full-img: явно задаём высоту страницы без отступов
    (
        "  .cover-full-img {\n    width: 210mm;\n    height: 297mm;\n    object-fit: cover;\n    object-position: center center;\n    display: block;\n    image-rendering: -webkit-optimize-contrast;\n  }",
        "  .cover-full-img {\n    width: 210mm;\n    height: 297mm;\n    min-height: 297mm;\n    object-fit: cover;\n    object-position: center center;\n    display: block;\n    image-rendering: -webkit-optimize-contrast;\n  }"
    ),
    # 3. base .page--cover: явный height чтобы не было min-height overflow
    (
        "  .page--cover {\n    padding: 0;\n    overflow: hidden;\n  }",
        "  .page--cover {\n    padding: 0;\n    height: 297mm;\n    min-height: 0;\n    overflow: hidden;\n  }"
    ),
]

log = []
for f in HTML_FILES:
    if not f.exists():
        log.append(f"MISSING: {f.name}")
        continue
    html = f.read_text(encoding="utf-8")
    changed = 0
    for old, new in FIXES:
        if old in html:
            html = html.replace(old, new, 1)
            changed += 1
    if changed:
        f.write_text(html, encoding="utf-8")
        log.append(f"FIXED ({changed} changes): {f.name}")
    else:
        log.append(f"OK (already fixed): {f.name}")

result = "\n".join(log)
(DESIGN / "_fix_cover_padding_log.txt").write_text(result, encoding="utf-8")
print("Done.")
