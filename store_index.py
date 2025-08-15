import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.helper import load_pdf, text_split, download_genAi

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = 'AIzaSyDc0-nLQCGSOHA2Y22RZj-YCliOO1_f6vM' 

api_key = os.environ.get("PINECONE_API_KEY") or "pcsk_47vyMh_QYDJNv155bd78wVoUxjUE6WNnEvW1BVKMhHBXB2LLAmdttr5DR3mF3XmBwZ4xzu"
os.environ["PINECONE_API_KEY"] = api_key  # Set for LangChain

pc = Pinecone(api_key=api_key)

index_name = "spbot"
DIM = 768  # Match embeddings dimension

# Create index if it doesn't exist
existing = [ix["name"] for ix in pc.list_indexes().get("indexes", [])]
if index_name not in existing:
    pc.create_index(
        name=index_name,
        dimension=DIM,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Load and process data
extracted_data = load_pdf('data/')
text_chunks = text_split(extracted_data)
embeddings = download_genAi()

# Create vector store
texts = [t.page_content for t in text_chunks]
docsearch = PineconeVectorStore.from_texts(
    texts=texts,
    embedding=embeddings,
    index_name=index_name,
)

print("Index created and documents uploaded successfully!")


