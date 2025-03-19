from fastapi import Depends, FastAPI
import neo4j
from neo4j_graphrag.llm import OpenAILLM as LLM
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings as Embeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.generation.graphrag import GraphRAG

#import fitz
# import uvicorn


app = FastAPI()

# def extract_text_from_pdf(pdf_path):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)

#     text = ""
#     # Iterate through each page
#     for page_number in range(len(pdf_document)):
#         page = pdf_document.load_page(page_number)
#         text += page.get_text()

#     return text


@app.get("/")
async def root():
    # pdf_path = "sample.pdf"
    # pdf_text = extract_text_from_pdf(pdf_path)

    return {"pdf_text":  "asd"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, server_headers=False)
