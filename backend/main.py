from fastapi import FastAPI
import config
import neo4j
from neo4j_graphrag.llm import OpenAILLM as LLM
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings as Embeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.indexes import create_vector_index
from neo4j_graphrag.generation.graphrag import GraphRAG
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
neo4j_driver = neo4j.GraphDatabase.driver(
    config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
)

llm = LLM(
    model_name=config.OPENAPI_MODEL,
    model_params={
        # "response_format": {"type": "json_object"},
        "temperature": 0
    },
    api_key=config.OPENAPI_KEY,
    base_url=config.OPENAPI_BASE_URL,
)

embedder = Embeddings(
    model=config.OPENAPI_EMBEDDING_MODEL,
    api_key=config.OPENAPI_KEY,
    base_url=config.OPENAPI_BASE_URL,
)


# def extract_text_from_pdf(pdf_path):
#      # Open the PDF file
#      pdf_document = fitz.open(pdf_path)

#       text = ""
#        # Iterate through each page
#        for page_number in range(len(pdf_document)):
#             page = pdf_document.load_page(page_number)
#             text += page.get_text()

#         return text


@app.get("/")
async def root():
    # pdf_path = "sample.pdf"
    # pdf_text = extract_text_from_pdf(pdf_path)
    # response = await ex_llm.ainvoke("Hello asdsad")
    # responsetwo = embedder.embed_query("Hello asdsad")

    # 1. Build KG and Store in Neo4j Database
    kg_builder_pdf = SimpleKGPipeline(
        llm=llm,
        driver=neo4j_driver,
        embedder=embedder,
        from_pdf=True,
    )
    await kg_builder_pdf.run_async(file_path="sample.pdf")
    create_vector_index(
        neo4j_driver,
        name="text_embeddings",
        label="Chunk",
        embedding_property="embedding",
        dimensions=1536,
        similarity_fn="cosine",
    )
    # 2. KG Retriever
    vector_retriever = VectorRetriever(
        neo4j_driver, index_name="text_embeddings", embedder=embedder
    )

    # 3. GraphRAG Class
    rag = GraphRAG(llm=llm, retriever=vector_retriever)

    # 4. Run
    response = rag.search("List all companies bhasker worked in?")
    print(response.answer)

    return {"pdf_text": response.answer}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, server_headers=False)
