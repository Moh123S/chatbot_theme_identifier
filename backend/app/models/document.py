class Document:
    def __init__(self, doc_id, filename, content, embeddings=None):
        self.doc_id = doc_id
        self.filename = filename
        self.content = content
        self.embeddings = embeddings or []
        
    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "filename": self.filename,
            "content": self.content,
            "embeddings": self.embeddings
        }