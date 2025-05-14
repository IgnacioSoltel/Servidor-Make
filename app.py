from flask import Flask, request, jsonify
import pdfplumber
import io
import os

app = Flask(__name__)


@app.route('/analizar', methods=['POST'])
def analizar_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({
            "status": "error",
            "mensaje": "No se envió ningún archivo PDF"
        }), 400

    try:
        pdf_bytes = file.read()
        texto = []

        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        texto.append(page_text)
                    else:
                        texto.append(f"[Página {i+1} sin texto detectable]")
                except Exception as e:
                    texto.append(f"[Error en página {i+1}: {str(e)}]")

        # Limitar el texto para evitar problemas con modelos o llamadas HTTP grandes
        MAX_CHARS = 10000
        full_text = "\n".join(texto)[:MAX_CHARS]

        return jsonify({"status": "ok", "texto_extraido": full_text})

    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)