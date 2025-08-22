import os
import tempfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
from docx2pdf import convert as docx2pdf_convert
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_IMAGE_EXT = {'png', 'jpg', 'jpeg'}
ALLOWED_PDF = {'pdf'}
ALLOWED_WORD = {'docx', 'doc'}

def allowed_file(filename, exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in exts

@app.route('/')
def home():
    return "PDFMaster Simple API Running!"

@app.route('/pdf-to-png', methods=['POST'])
def pdf_to_png():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename, ALLOWED_PDF):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)
        try:
            images = convert_from_path(pdf_path)
        except Exception as e:
            return jsonify({'error': f'Conversion error: {str(e)}'}), 500

        output_paths = []
        for idx, img in enumerate(images):
            out_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_page_{idx+1}.png")
            img.save(out_path, 'PNG')
            output_paths.append(out_path)

        if len(output_paths) == 1:
            return send_file(output_paths[0], as_attachment=True)
        else:
            import zipfile
            zipname = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}_pngs.zip")
            with zipfile.ZipFile(zipname, 'w') as zipf:
                for file_path in output_paths:
                    zipf.write(file_path, os.path.basename(file_path))
            return send_file(zipname, as_attachment=True)
    else:
        return jsonify({'error': 'Invalid file'}), 400

@app.route('/png-to-pdf', methods=['POST'])
def png_to_pdf():
    files = request.files.getlist('files')
    image_paths = []
    for file in files:
        if file and allowed_file(file.filename, ALLOWED_IMAGE_EXT):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)
            image_paths.append(img_path)
    if not image_paths:
        return jsonify({'error': 'No valid images uploaded'}), 400

    images = []
    for p in image_paths:
        try:
            images.append(Image.open(p).convert('RGB'))
        except Exception:
            continue
    if not images:
        return jsonify({'error': 'No valid images found'}), 400

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'combined.pdf')
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    return send_file(pdf_path, as_attachment=True)

@app.route('/pdf-to-word', methods=['POST'])
def pdf_to_word():
    # NOTE: docx2pdf is for docx<->pdf, not pdf->docx. So this is a placeholder.
    return jsonify({'error': 'PDF to Word conversion is not fully supported with free open-source tools. Please use a dedicated online service or premium API for this feature.'}), 400

@app.route('/word-to-pdf', methods=['POST'])
def word_to_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename, ALLOWED_WORD):
        filename = secure_filename(file.filename)
        docx_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(docx_path)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 1)[0] + ".pdf")
        try:
            docx2pdf_convert(docx_path, pdf_path)
        except Exception as e:
            return jsonify({'error': f'Conversion error: {str(e)}'}), 500
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(debug=True)