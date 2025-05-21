from app.services.ocr_service import extract_text
from app.services.vector_store import VectorStore
from app.models.document import Document
import os
import uuid
import aiofiles

class DocumentProcessor:
    def __init__(self):
        self.vector_store = VectorStore()
        self.upload_dir = "data/uploads"
        os.makedirs(self.upload_dir, exist_ok=True)
        self.documents = {}
    
    async def process_document(self, file):
        try:
            doc_id = str(uuid.uuid4())
            filename = file.filename
            file_path = os.path.join(self.upload_dir, filename)
            
            # Save file asynchronously
            async with aiofiles.open(file_path, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)
            
            content = extract_text(file_path)
            doc = Document(doc_id, filename, content)
            self.vector_store.add_document(doc_id, content)
            self.documents[doc_id] = doc
            return doc
        except Exception as e:
            raise Exception(f"Error processing document {filename}: {str(e)}")
    
    def get_all_documents(self):
        return list(self.documents.values())