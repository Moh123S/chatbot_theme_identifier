from langchain_groq import ChatGroq  # Updated import
   from langchain.prompts import PromptTemplate
   import os

   class ThemeIdentifier:
       def __init__(self):
           self.llm = ChatGroq(
               groq_api_key=os.getenv("GROQ_API_KEY"),
               model_name="llama3-8b-8192"
           )
           self.prompt_template = PromptTemplate(
               input_variables=["responses"],
               template="Given the following document responses:\n{responses}\n\nIdentify common themes across these responses. Provide a list of themes with supporting document IDs."
           )
       
       async def identify_themes(self, responses):
           try:
               response_text = "\n".join([f"Doc {r['document_id']}: {r['answer']}" for r in responses])
               prompt = self.prompt_template.format(responses=response_text)
               result = await self.llm.ainvoke(prompt)
               themes = result.content.split("\n")
               return [theme.strip() for theme in themes if theme.strip()]
           except Exception as e:
               raise Exception(f"Error identifying themes: {str(e)}")