# -*- coding: utf-8 -*-
"""
Копирует 9 готовых обложек в design/assets/workbook/
и заменяет секцию обложки во всех 9 HTML воркбуках.
"""
import re
import shutil
from pathlib import Path

ASSETS_SRC = Path(r"C:\Users\user\.cursor\projects\c-Users-user-Desktop-CURSOR-Kati-Agency-kati-agency-site\assets")
DESIGN = Path(r"C:\Users\user\Desktop\CURSOR\design")
ASSETS_DST = DESIGN / "assets" / "workbook"
ASSETS_DST.mkdir(parents=True, exist_ok=True)

# Маппинг: имя файла из assets → имя обложки CHS + архетип для alt
COVERS = [
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_1_-3fd43852-1748-4486-b9ab-ac2886aaeb31.png",  "cover-chs1.png", "ЛИДЕР"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_2_-aff8ef3a-f374-4a77-b74f-4f182d265eb2.png",  "cover-chs2.png", "ДИПЛОМАТ"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_3_-9c59ae6e-531c-41f0-9d13-f76247389375.png",  "cover-chs3.png", "ТВОРЕЦ"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_4_-38a8f8d6-f28a-41eb-9fcc-a3e29373714b.png",  "cover-chs4.png", "АРХИТЕКТОР"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_5_-d35dd8cf-12de-4ddb-8960-969457c6ef7a.png",  "cover-chs5.png", "ИССЛЕДОВАТЕЛЬ"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images___________________-f6378d81-6bbe-4632-8a6d-6e78384938ed.png", "cover-chs6.png", "НАСТАВНИК"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_7_-02f5dea7-0ede-452f-ae2c-06291403a34d.png",  "cover-chs7.png", "МУДРЕЦ"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_8_-8102bbc8-dd13-4cac-b4b6-f085313fc289.png",  "cover-chs8.png", "УПРАВЛЕНЕЦ"),
    ("c__Users_user_AppData_Roaming_Cursor_User_workspaceStorage_31cc6da8190f0fddc6fdbcdb495cca6c_images_9_-e32ba7ab-e482-42a6-81ec-b93bc8487421.png",  "cover-chs9.png", "ГУМАНИСТ"),
]

# HTML файлы в порядке CHS1-9
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

NEW_COVER_CSS = """
  /* —— СТР. 1 · ОБЛОЖКА — ПОЛНОЭКРАННОЕ ФОТО —— */
  .page--cover {
    padding: 0;
    overflow: hidden;
  }
  .page--cover .page-bg,
  .page--cover .page-veil,
  .page--cover .page-photo { display: none; }
  .cover-full-img {
    width: 210mm;
    height: 297mm;
    object-fit: cover;
    object-position: center center;
    display: block;
    image-rendering: -webkit-optimize-contrast;
  }
"""

OLD_COVER_CSS_PATTERN = re.compile(
    r"/\* —— СТР\. 1 · ОБЛОЖКА.*?\.page-photo \{.*?\}",
    re.DOTALL,
)


def cover_section(img_filename: str, archetype: str) -> str:
    return f"""<!-- СТР. 1 · ОБЛОЖКА -->
<section class="page page--cover">
  <img class="cover-full-img"
       src="assets/workbook/{img_filename}"
       alt="SOUL METHOD | {archetype}">
</section>"""


OLD_COVER_SECTION_PATTERN = re.compile(
    r"<!-- СТР\. 1 · ОБЛОЖКА -->.*?</section>",
    re.DOTALL,
)


def main():
    log = []

    # 1. Копируем обложки
    for src_name, dst_name, archetype in COVERS:
        src = ASSETS_SRC / src_name
        dst = ASSETS_DST / dst_name
        if src.exists():
            shutil.copy2(src, dst)
            log.append(f"OK cover: {dst_name} ({dst.stat().st_size // 1024} KB)")
        else:
            log.append(f"MISSING source: {src_name}")

    # 2. Обновляем HTML
    for i, (html_path, (_, dst_name, archetype)) in enumerate(zip(HTML_FILES, COVERS)):
        if not html_path.exists():
            log.append(f"MISSING html: {html_path.name}")
            continue

        html = html_path.read_text(encoding="utf-8")

        # Заменяем CSS обложки
        if OLD_COVER_CSS_PATTERN.search(html):
            html = OLD_COVER_CSS_PATTERN.sub(NEW_COVER_CSS.strip(), html, count=1)
        else:
            # Вставляем перед @page
            html = html.replace("  @page {", NEW_COVER_CSS + "\n  @page {", 1)

        # Заменяем HTML секцию обложки
        new_section = cover_section(dst_name, archetype)
        html = OLD_COVER_SECTION_PATTERN.sub(new_section, html, count=1)

        html_path.write_text(html, encoding="utf-8")
        log.append(f"OK html: {html_path.name} → {archetype}")

    result = "\n".join(log)
    (DESIGN / "_apply_covers_log.txt").write_text(result, encoding="utf-8")
    print("Done. See _apply_covers_log.txt")


if __name__ == "__main__":
    main()
