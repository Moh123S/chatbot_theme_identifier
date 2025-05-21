from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from app.services.vector_store import VectorStore
import os

class QueryProcessor:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )
        self.prompt_template = PromptTemplate(
            input_variables=["context", "query"],
            template="Given the following document content:\n{context}\n\nAnswer the query: {query}\nProvide a concise answer and cite the specific paragraph or page if possible."
        )
    
    async def process_query(self, query):
        try:
            results = self.vector_store.search(query, k=5)
            responses = []
            
            for doc, score in results:
                context = doc.page_content
                prompt = self.prompt_template.format(context=context, query=query)
                response = await self.llm.ainvoke(prompt)
                answer = response.content
                citation = f"Document {doc.metadata['doc_id']}, Page {context.split('[Page')[1].split(']')[0]}"
                responses.append({
                    "document_id": doc.metadata["doc_id"],
                    "answer": answer,
                    "citation": citation,
                    "score": score
                })
            
            return responses
        except Exception as e:
            raise Exception(f"Error processing query: {str(e)}")