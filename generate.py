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

        page = (template
                .replace("{{NUM}}", str(num))
                .replace("{{ROMAN}}", to_roman(num))
                .replace("{{TITLE}}", title)
                .replace("{{AUDIO}}", f"../../audio/{audio_file}")
                .replace("{{PORTRAIT_CLASS}}", portrait_class)
                .replace("{{PORTRAIT_IMG}}", portrait_img))

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
