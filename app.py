from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import io
import os

app = Flask(__name__)

@app.route('/analizar', methods=['POST'])
def analizar_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({"status": "error", "mensaje": "No se envió ningún archivo PDF"}), 400

    try:
        pdf_bytes = file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))

        texto = []
        for page in reader.pages:
            texto.append(page.extract_text() or "")

        full_text = "\n".join(texto)

        return jsonify({
            "status": "ok",
            "texto_extraido": full_text
        })

    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
