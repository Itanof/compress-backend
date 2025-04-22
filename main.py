from flask import Flask, request, send_file
import io
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    uploaded = request.files.get('file')
    if not uploaded:
        return "No file uploaded", 400

    reader = PdfReader(uploaded)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.compress_content_streams()

    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    return send_file(
        buf,
        as_attachment=True,
        download_name='compressed.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
