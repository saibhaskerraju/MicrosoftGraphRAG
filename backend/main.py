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
import fitz
import spacy
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

nlp = spacy.load("en_core_web_sm")


# Authenticate the client using your key and endpoint
def authenticate_client():
	ta_credential = AzureKeyCredential(config.AZURE_LANGUAGE_KEY)
	text_analytics_client = TextAnalyticsClient(
		endpoint=config.AZURE_LANGUAGE_ENDPOINT, credential=ta_credential
	)
	return text_analytics_client


client = authenticate_client()


app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["GET"],
	allow_headers=["*"],
)
neo4j_driver = neo4j.GraphDatabase.driver(
	config.NEO4J_URI
	# , auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
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


def create_entity(entity_text, entity_category):
	with neo4j_driver.session() as session:
		session.run(
			"MERGE (e:Entity {text: $text, category: $category})",
			text=entity_text,
			category=entity_category,
		)


def create_relationship(entity1_text, entity2_text, relationship):
	with neo4j_driver.session() as session:
		session.run(
			"""
            MATCH (e1:Entity {text: $entity1_text})
            MATCH (e2:Entity {text: $entity2_text})
            MERGE (e1)-[:RELATIONSHIP {type: $relationship}]->(e2)
            """,
			entity1_text=entity1_text,
			entity2_text=entity2_text,
			relationship=relationship,
		)


def extract_text_from_pdf(pdf_path):
	# Open the PDF file
	pdf_document = fitz.open(pdf_path)
	text = ""
	# Iterate through each page
	for page_number in range(len(pdf_document)):
		page = pdf_document.load_page(page_number)
		text += page.get_text()

	return text


@app.get("/azure")
async def entities():
	pdf_path = "sample.pdf"
	pdf_text = extract_text_from_pdf(pdf_path)
	response = client.recognize_entities([pdf_text])
	for doc in response:
		if not doc.is_error:
			entities = doc.entities
			for entity in entities:
				create_entity(entity.text, entity.category)

			if len(entities) > 1:
				for i in range(len(entities) - 1):
					create_relationship(
						entities[i].text, entities[i + 1].text, "RELATED_TO"
					)

	return {"message": "Entities and relationships created in Neo4j."}


@app.get("/spacy")
async def pdf():
	pdf_path = "sample.pdf"
	pdf_text = extract_text_from_pdf(pdf_path)
	doc = nlp(pdf_text)
	entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
	pos_tags = [{"text": token.text, "pos": token.pos_} for token in doc]
	return {"entities": entities, "pos_tags": pos_tags}


@app.get("/test")
async def test():
	response = await llm.ainvoke("Hello asdsad")
	responsetwo = embedder.embed_query("Hello asdsad")
	return {"response": response, "responsetwo": responsetwo}

@app.get("/run")
async def run():
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
	response = rag.search("give me details on paypal financial domain. a brief overview")
	print(response.answer)
	return {"response": response.answer}


@app.get("/")
async def root():
	# 1. Build KG and Store in Neo4j Database
	kg_builder_pdf = SimpleKGPipeline(
		llm=llm,
		driver=neo4j_driver,
		embedder=embedder,
		from_pdf=True,
	)
	await kg_builder_pdf.run_async(file_path="sampletwo.pdf")
	

	return {"response": "Data inserted into Neo4j"}



# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, server_headers=False)
