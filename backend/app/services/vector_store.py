from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

class VectorStore:
    def __init__(self, persist_directory="data/chroma"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory=persist_directory
        )
       
    def add_document(self, doc_id, content):
        try:
            self.vector_store.add_texts(
                texts=[content],
                ids=[doc_id],
                metadatas=[{"doc_id": doc_id}]
            )
        except Exception as e:
            raise Exception(f"Error adding document {doc_id} to vector store: {str(e)}")
       
    def search(self, query, k=5):
        try:
            results = self.vector_store.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            raise Exception(f"Error searching vector store: {str(e)}")