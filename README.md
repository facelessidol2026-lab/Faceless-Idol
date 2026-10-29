# Faceless-Idol — Soundtrack-QR kitab sistemi

**AZ** | **RU** | **EN**

---

## AZ — Azərbaycan dili

Bu layihə kitabın 15 vahidə (track) üçün səhifə və QR-kod sistemi yaradır. Hər səhifədə audio trək läuft və 독립 QR-kod var.

### Quraşdırma

```bash
pip install -r requirements.txt
```

### ƏƏDƏLƏDİRLƏNМЕ addımları

1. `chapters.json`-i yoxlayın — 15 səhnə: nömrə, başlıq və audio fayl (`track1.wav` … `track15.wav`).
2. MP3/WAV fayllarını `docs/audio/` directoriesna yükləyin.
3. Generatoru işə salın:

```bash
cd soundtrack-book
python generate.py --base-url https://facelessidol2026-lab.github.io/Faceless-Idol
```

Yaradılır:
- `docs/ch/<N>/index.html` — hər səhnə üçün indipendənt plejer səhifəsi
- `docs/qr/ch<N>.png` — vektorlu QR-kod, o səhifəyə yönləndirir

### GitHub Pages-də públicas edin

1. Dəyişiklikləri `main` filialına göndərin (`chapters.json`, `template.html`, `generate.py`, `README.md`, `docs/`).
2. Repository → Settings → Pages → Source: **Deploy from branch**, filial `main`, folder `/docs`.
3. Sayt: `https://facelessidol2026-lab.github.io/Faceless-Idol/ch/1/` və s.

### QR-kodları

`docs/qr/ch1.png` … `ch15.png` fayllarını kitabın məketinə daxil edin.

---

## RU — Русский язык

Система саундтрека-QR для книги: 15 глав, каждая со своей страницей и QR-кодом.

### Установка

```bash
pip install -r requirements.txt
```

### Шаги

1. Проверьте `chapters.json` — 15 глав: номер, название, аудиофайл (`track1.wav` … `track15.wav`).
2. Положите аудио в `docs/audio/`.
3. Запустите генератор:

```bash
cd soundtrack-book
python generate.py --base-url https://facelessidol2026-lab.github.io/Faceless-Idol
```

Создаётся:
- `docs/ch/<N>/index.html` — страница главы с плеером
- `docs/qr/ch<N>.png` — векторный QR-код на страницу главы

### Публикация на GitHub Pages

1. Запушьте в ветку `main` (`chapters.json`, `template.html`, `generate.py`, `README.md`, `docs/`).
2. Repository → Settings → Pages → Source: **Deploy from branch**, ветка `main`, папка `/docs`.
3. Сайт: `https://facelessidol2026-lab.github.io/Faceless-Idol/ch/1/` и т.д.

### QR-коды

Вставьте `docs/qr/ch1.png` … `ch15.png` в макет книги.

---

## EN — English language

Soundtrack-QR system for the book: 15 chapters, each with its own page and QR code.

### Installation

```bash
pip install -r requirements.txt
```

### Steps

1. Check `chapters.json` — 15 chapters: number, title, audio file (`track1.wav` … `track15.wav`).
2. Put audio into `docs/audio/`.
3. Run the generator:

```bash
cd soundtrack-book
python generate.py --base-url https://facelessidol2026-lab.github.io/Faceless-Idol
```

Creates:
- `docs/ch/<N>/index.html` — chapter page with player
- `docs/qr/ch<N>.png` — vector QR code to the chapter page

### Publish on GitHub Pages

1. Push to branch `main` (`chapters.json`, `template.html`, `generate.py`, `README.md`, `docs/`).
2. Repository → Settings → Pages → Source: **Deploy from branch**, branch `main`, folder `/docs`.
3. Site: `https://facelessidol2026-lab.github.io/Faceless-Idol/ch/1/` etc.

### QR codes

Insert `docs/qr/ch1.png` … `ch15.png` into the book layout.

---

### Dizayn

`template.html` və `generate.py` təsəəlli dizayndır — onları dəyişdirmək məməludu deyil.
