from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.core.document_processor import DocumentProcessor
from app.core.query_processor import QueryProcessor
from app.core.theme_identifier import ThemeIdentifier

router = APIRouter()
document_processor = DocumentProcessor()
query_processor = QueryProcessor()
theme_identifier = ThemeIdentifier()

class QueryRequest(BaseModel):
    query: str

@router.post("/upload")
async def upload_documents(documents: list[UploadFile] = File(...)):
    try:
        for file in documents:
            await document_processor.process_document(file)
        return JSONResponse(content={"message": "Documents uploaded successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents")
async def get_documents():
    try:
        documents = document_processor.get_all_documents()
        return [{"doc_id": doc.doc_id, "filename": doc.filename} for doc in documents]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query_documents(request: QueryRequest):
    try:
        responses = await query_processor.process_query(request.query)
        themes = await theme_identifier.identify_themes(responses)
        return {"responses": responses, "themes": themes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))