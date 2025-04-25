from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import io
from pypdf import PdfReader, PdfWriter

app = Flask(__name__)
CORS(app)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    try:
        uploaded = request.files.get('file')
        if not uploaded:
            return jsonify(error="No file uploaded"), 400

        reader = PdfReader(uploaded)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # removed compress_content_streams()

        buf = io.BytesIO()
        writer.write(buf)
        buf.seek(0)
        return send_file(
            buf,
            as_attachment=True,
            download_name='compressed.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        # This will return the actual Python error to your frontend
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
