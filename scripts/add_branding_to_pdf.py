#!/usr/bin/env python3
"""
Додає на останню сторінку PDF білий кириличний клікабельний текст:
"Офіційний представник в Україні - PARKAN.UA"
Відступи: зліва 2 см, знизу 5 см.
Зберігає результати в documents/crystal-tourniket/branded/
"""

import os
import sys
from pathlib import Path

# Конвертація см в пункти (1 см ≈ 28.35 pt)
CM_TO_PT = 28.35
LEFT_CM = 2
BOTTOM_CM = 5
TEXT = "Офіційний представник в Україні - PARKAN.UA"
LINK_URL = "https://parkan.ua"

# Шляхи до шрифтів з підтримкою кирилиці (перший існуючий використовується)
CYRILLIC_FONT_PATHS = [
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",  # macOS
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",       # Linux
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",                          # Windows
]


def find_cyrillic_font():
    """Повертає шлях до першого знайденого шрифту з кирилицею."""
    for path in CYRILLIC_FONT_PATHS:
        if os.path.isfile(path):
            return path
    return None


def create_overlay_pdf(page_width_pt: float, page_height_pt: float, font_path: str) -> bytes:
    """Створює PDF-шар з білим кириличним текстом і клікабельним посиланням."""
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from io import BytesIO

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width_pt, page_height_pt))
    pdfmetrics.registerFont(TTFont("CyrillicFont", font_path))
    c.setFont("CyrillicFont", 10)
    c.setFillColorRGB(1, 1, 1)  # білий

    x = LEFT_CM * CM_TO_PT
    y = BOTTOM_CM * CM_TO_PT
    text_width = c.stringWidth(TEXT, "CyrillicFont", 10)
    text_height = 12

    # Спочатку посилання (аннотація), потім текст поверх
    c.linkURL(LINK_URL, (x, y, x + text_width, y + text_height), relative=1)
    c.drawString(x, y, TEXT)

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def add_branding_to_pdf(input_path: Path, output_path: Path, font_path: str) -> bool:
    """Додає брендинг на останню сторінку PDF і зберігає в output_path."""
    from pypdf import PdfReader, PdfWriter
    from io import BytesIO

    reader = PdfReader(input_path)
    writer = PdfWriter()
    num_pages = len(reader.pages)
    if num_pages == 0:
        print(f"  Пропущено (немає сторінок): {input_path.name}")
        return False

    last_page = reader.pages[-1]
    page_width = float(last_page.mediabox.width)
    page_height = float(last_page.mediabox.height)

    # Overlay PDF
    overlay_bytes = create_overlay_pdf(page_width, page_height, font_path)
    overlay_reader = PdfReader(BytesIO(overlay_bytes))
    overlay_page = overlay_reader.pages[0]

    # Копіюємо всі сторінки; на останню накладаємо overlay
    for i in range(num_pages):
        page = reader.pages[i]
        if i == num_pages - 1:
            page.merge_page(overlay_page)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)
    return True


def main():
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    source_dir = project_root / "documents" / "crystal-tourniket"
    out_dir = source_dir / "branded"

    font_path = find_cyrillic_font()
    if not font_path:
        print("Помилка: не знайдено шрифт з підтримкою кирилиці.")
        print("Перевірте наявність одного з:", CYRILLIC_FONT_PATHS)
        sys.exit(1)

    if not source_dir.is_dir():
        print(f"Помилка: папка не знайдена: {source_dir}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(source_dir.glob("*.pdf"))

    if not pdf_files:
        print("PDF-файли в crystal-tourniket не знайдено.")
        sys.exit(0)

    print("Шрифт:", font_path)
    print("Текст на останній сторінці:", TEXT)
    print("Відступи: зліва 2 см, знизу 5 см. Результат у:", out_dir)
    print()

    for pdf_path in sorted(pdf_files):
        out_path = out_dir / pdf_path.name
        try:
            if add_branding_to_pdf(pdf_path, out_path, font_path):
                print("OK:", pdf_path.name, "->", out_path.name)
        except Exception as e:
            print("Помилка", pdf_path.name, ":", e)

    print("\nГотово. Файли з брендингом у:", out_dir)


if __name__ == "__main__":
    main()
