from flask import Flask, request, jsonify, redirect, send_from_directory, send_file
from pathlib import Path
from search_engine import search_query_across_batches

app = Flask(__name__)

PDF_DIR = Path("static/pdfs")

@app.route("/api/search")
def search():
    query = request.args.get("query")
    top_k = int(request.args.get("top_k", 5))
    results = search_query_across_batches(query, top_k=top_k)
    return jsonify(results)


@app.route("/api/open-pdf")
def open_pdf():
    filename = request.args.get("file")
    page = request.args.get("page", "1")  # optional, could be passed in metadata
    pdf_path = PDF_DIR / filename

    if not pdf_path.exists():
        return f"❌ File not found: {filename}", 404

    # Send file as response (inline viewing if browser supports it)
    return send_file(pdf_path, as_attachment=False, mimetype="application/pdf")



if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)