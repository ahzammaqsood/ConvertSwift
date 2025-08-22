# PDFMaster Flask Backend

## Features

- PDF to PNG (multi-page support, output as ZIP if multi-page)
- PNG/JPG to PDF (multiple images to one PDF)
- Word to PDF (docx to PDF)
- PDF to Word (not fully supported in free open-source, see note below)

## Quick Start (Local)

```sh
pip install -r requirements.txt
python app.py
```

## API Endpoints

- `/pdf-to-png` (POST, file: PDF)
- `/png-to-pdf` (POST, files: images)
- `/word-to-pdf` (POST, file: DOCX)
- `/pdf-to-word` (POST, file: PDF) — NOT SUPPORTED in open-source (see below)

## PDF to Word Note

- Free open-source mein PDF to DOCX conversion fully accurate nahi hota, aur docx2pdf yeh nahi karta.  
- Is feature ke liye premium APIs (SmallPDF, PDF.co, Cloudmersive, etc.) use karni parti hai.  
- Baaki 3 conversions 100% open-source hain.

## Deploy on Render.com

1. Fork/clone this repo.
2. Push to your GitHub.
3. Go to [Render.com](https://render.com), New > Web Service.
4. Connect your repo, select Python.
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python app.py`
7. Region: Closest to you.
8. Free plan select karen, "Create Web Service".
9. Done! API base URL mil jayegi.

## Frontend Integration

- Aap apne frontend se `fetch` ya `axios` use kar ke files upload kar sakte hain.
- API endpoints pe POST request bhejein.
