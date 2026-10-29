#!/usr/bin/env python3
"""
Генерирует:
  docs/ch/<N>/index.html  — сəhifə böyükilə plejerlə
  docs/qr/ch<N>.png       — QR-kod, o səhifəyə yönləndirir

İstifadə:
  python generate.py --base-url https://USERNAME.github.io/REPO
"""
import json
import argparse
from pathlib import Path
import qrcode

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"

THEME_MAP = {
    1: "theme-prolog",
    2: "theme-story",
    3: "theme-arab",
    4: "theme-spanish",
    5: "theme-italian",
    6: "theme-english",
    7: "theme-indian",
    8: "theme-turkish",
    9: "theme-chinese",
    10: "theme-german",
    11: "theme-jewish",
    12: "theme-african",
    13: "theme-german",
    14: "theme-human",
    15: "theme-epilog",
}

# Реальные орнаменты (изображения) для глав, где скачаны из интернета
ORNAMENT_IMAGES = {
    4: "spanish_moorish_tile.svg",
    5: "italian_acanthus.png",
    6: "english_tudor_rose.svg",
    7: "indian_mandala.svg",
    8: "turkish_tulip.svg",
    9: "chinese_dragon.svg",
    11: "jewish_menorah.svg",
    12: "african_gye_nyame.svg",
}

# Цвета туманности и души для каждой главы (астральная палитра + традиционные цвета)
NEBULA_COLORS = {
    1: "#B08D57", 2: "#8A8378", 3: "#1B5E20", 4: "#1565C0",
    5: "#BF360C", 6: "#C62828", 7: "#FF6F00", 8: "#00695C",
    9: "#C62828", 10: "#424242", 11: "#1976D2", 12: "#795548",
    13: "#424242", 14: "#757575", 15: "#B08D57",
}
SOUL_COLORS = {
    1: "#FFD700", 2: "#C0C0C0", 3: "#90EE90", 4: "#87CEEB",
    5: "#FFA07A", 6: "#FF6B6B", 7: "#FFD700", 8: "#40E0D0",
    9: "#FF4500", 10: "#A9A9A9", 11: "#87CEFA", 12: "#DEB887",
    13: "#A9A9A9", 14: "#FFFFFF", 15: "#FFD700",
}

# Символы профессий (SVG-иконки)
PROFESSION_ICONS = {
    1: '<svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
    2: '<svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 016.5 17H20M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>',
    3: '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 100 20 10 10 0 000-20zm0 18a8 8 0 110-16 8 8 0 010 16z"/><path d="M12 6v6l4 2"/></svg>',
    4: '<svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>',
    5: '<svg viewBox="0 0 24 24"><path d="M12 19l7-7 3 3-7 7-3-3zM18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5zM2 2l7.5 1.5L13 8"/></svg>',
    6: '<svg viewBox="0 0 24 24"><path d="M17 3a2.828 2.828 0 114 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>',
    7: '<svg viewBox="0 0 24 24"><path d="M9 18V5l12-2v13M9 9l12-2"/></svg>',
    8: '<svg viewBox="0 0 24 24"><path d="M14.5 17.5L3 6.5l3-3 11.5 11M14.5 17.5L18 21l3-3-3.5-3.5M14.5 17.5l-4-4"/></svg>',
    9: '<svg viewBox="0 0 24 24"><path d="M5 8l6 6M4 14l6-6 2-3 4-1 1 4-3 2-6 6H4v-2z"/></svg>',
    10: '<svg viewBox="0 0 24 24"><path d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18"/></svg>',
    11: '<svg viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>',
    12: '<svg viewBox="0 0 24 24"><path d="M15 4V2M15 16v-2M8 9h2M20 9h2M8 15l1.5-1.5M18.5 5.5L20 4M8 3l1.5 1.5M18.5 12.5L20 14"/></svg>',
    13: '<svg viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5-10-5zM6 12v5c3 3 9 3 12 0v-5"/></svg>',
    14: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M6 21v-2a4 4 0 014-4h4a4 4 0 014 4v2"/></svg>',
    15: '<svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
}

PROFESSION_NAMES = {
    1: "", 2: "", 3: "Gəzər",
    4: "Vurğun", 5: "Rəssam", 6: "Yazıçı", 7: "Musiqiçi",
    8: "Döyüşçü", 9: "Dilçi", 10: "İxtiraçı", 11: "Tacir",
    12: "Maq", 13: "Tərbiyəçı", 14: "İnsan", 15: "",
}

MAP_BADGES = {
    1: "", 2: "", 3: "Ərəbistan", 4: "İspaniya", 5: "İtaliya",
    6: "İngiltərə", 7: "Hindistan", 8: "Türkiyə", 9: "Çin",
    10: "Almaniya", 11: "Yəhudi", 12: "Afrika", 13: "Almaniya",
    14: "Bəşəriyyət", 15: "",
}

ROMAN_MAP = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]

def to_roman(n: int) -> str:
    result = ""
    for value, symbol in ROMAN_MAP:
        while n >= value:
            result += symbol
            n -= value
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True,
                         help="məs. https://kenny.github.io/book-soundtrack")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    chapters = json.loads((ROOT / "chapters.json").read_text(encoding="utf-8"))
    template = (ROOT / "template.html").read_text(encoding="utf-8")

    ch_dir = DOCS / "ch"
    qr_dir = DOCS / "qr"
    ch_dir.mkdir(parents=True, exist_ok=True)
    qr_dir.mkdir(parents=True, exist_ok=True)

    for chapter in chapters:
        num = chapter["num"]
        title = chapter["title"]
        audio_file = chapter["file"]

        has_portrait = num >= 3 and num <= 14
        portrait_class = " has-portrait" if has_portrait else ""
        portrait_img = (f'<div class="portrait"><img src="../../assets/pictures/person_{num}.jpg" '
                        f'alt="{title}"></div>' if has_portrait else "")
        theme = THEME_MAP.get(num, "theme-default")

        # Орнамент: реальное изображение или CSS-паттерн
        if num in ORNAMENT_IMAGES:
            ornament_file = ORNAMENT_IMAGES[num]
            ornament_style = (f"background-image: url('../../assets/ornaments/{ornament_file}'); "
                              f"background-size: 200px 200px; background-repeat: repeat; opacity: 0.08;")
        else:
            ornament_style = ""

        # Профессия
        profession_icon = PROFESSION_ICONS.get(num, "")
        profession_name = PROFESSION_NAMES.get(num, "")
        if profession_name:
            profession_html = f'{profession_icon}<span>{profession_name}</span>'
        else:
            profession_html = ""

        # Карта/место
        map_badge = MAP_BADGES.get(num, "")

        # Цвета туманности и души
        nebula_color = NEBULA_COLORS.get(num, "#B08D57")
        soul_color = SOUL_COLORS.get(num, "#FFD700")

        page = (template
                .replace("{{NUM}}", str(num))
                .replace("{{ROMAN}}", to_roman(num))
                .replace("{{TITLE}}", title)
                .replace("{{AUDIO}}", f"../../audio/{audio_file}")
                .replace("{{PORTRAIT_CLASS}}", portrait_class)
                .replace("{{PORTRAIT_IMG}}", portrait_img)
                .replace("{{THEME}}", theme)
                .replace("{{ORNAMENT_STYLE}}", ornament_style)
                .replace("{{PROFESSION_ICON}}", profession_icon)
                .replace("{{PROFESSION_NAME}}", profession_name)
                .replace("{{PROFESSION_HTML}}", profession_html)
                .replace("{{MAP_BADGE}}", map_badge)
                .replace("{{NEBULA_COLOR}}", nebula_color)
                .replace("{{SOUL_COLOR}}", soul_color))

        page_dir = ch_dir / str(num)
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(page, encoding="utf-8")

        chapter_url = f"{base_url}/ch/{num}/"
        img = qrcode.make(chapter_url, box_size=12, border=3)
        img.save(qr_dir / f"ch{num}.png")

        print(f"Bəb {num:>2} | {title:<30} | {chapter_url}")

    print(f"\nHazırdır: {len(chapters)} səhifə docs/ch/-də, {len(chapters)} QR-kod docs/qr/-də")

if __name__ == "__main__":
    main()
