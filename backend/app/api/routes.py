from flask import Blueprint, request, jsonify, render_template
from app.core.document_processor import DocumentProcessor
from app.core.query_processor import QueryProcessor
from app.core.theme_identifier import ThemeIdentifier

api_bp = Blueprint("api", __name__)
document_processor = DocumentProcessor()
query_processor = QueryProcessor()
theme_identifier = ThemeIdentifier()

@api_bp.route("/upload", methods=["POST"])
def upload_documents():
    try:
        files = request.files.getlist("documents")
        for file in files:
            document_processor.process_document(file)
        return jsonify({"message": "Documents uploaded successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/documents", methods=["GET"])
def get_documents():
    try:
        documents = document_processor.get_all_documents()
        return jsonify([{"doc_id": doc.doc_id, "filename": doc.filename} for doc in documents])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/query", methods=["POST"])
def query_documents():
    try:
        data = request.get_json()
        query = data.get("query", "")
        responses = query_processor.process_query(query)
        themes = theme_identifier.identify_themes(responses)
        return jsonify({"responses": responses, "themes": themes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500