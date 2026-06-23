# -*- coding: utf-8 -*-
"""Восстанавливает базовый CSS .page-photo во всех 9 HTML воркбуках."""
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

# Удаляем дубль cover-full-img и восстанавливаем .page-photo base

OLD_DUPLICATE = """.cover-full-img {
    width: 210mm;
    height: 297mm;
    object-fit: cover;
    object-position: center center;
    display: block;
    image-rendering: -webkit-optimize-contrast;
  }
  .cover-full-img {
    width: 210mm;
    height: 297mm;
    object-fit: cover;
    object-position: center center;
    display: block;
    image-rendering: -webkit-optimize-contrast;
  }"""

NEW_SINGLE = """.cover-full-img {
    width: 210mm;
    height: 297mm;
    object-fit: cover;
    object-position: center center;
    display: block;
    image-rendering: -webkit-optimize-contrast;
  }

  /* —— .page-photo используется на всех страницах с фоном —— */
  .page-photo {
    position: absolute;
    inset: 0;
    z-index: 0;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
  }"""

log = []
for f in HTML_FILES:
    if not f.exists():
        log.append(f"MISSING: {f.name}")
        continue
    html = f.read_text(encoding="utf-8")
    if OLD_DUPLICATE in html:
        html = html.replace(OLD_DUPLICATE, NEW_SINGLE, 1)
        f.write_text(html, encoding="utf-8")
        log.append(f"FIXED: {f.name}")
    elif ".page-photo {" not in html:
        # на случай если структура чуть другая — просто вставляем перед .page--author
        html = html.replace(
            ".page--author .page-photo {",
            ".page-photo {\n    position: absolute;\n    inset: 0;\n    z-index: 0;\n    background-size: cover;\n    background-position: center;\n    background-repeat: no-repeat;\n  }\n\n  .page--author .page-photo {",
            1,
        )
        f.write_text(html, encoding="utf-8")
        log.append(f"RESTORED: {f.name}")
    else:
        log.append(f"OK (no change needed): {f.name}")

(DESIGN / "_fix_photo_css_log.txt").write_text("\n".join(log), encoding="utf-8")
print("Done.")
