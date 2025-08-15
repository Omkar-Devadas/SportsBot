from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.prompt import prompt_template  # Import from your prompt.py (adjust if needed)
from langchain_core.prompts import PromptTemplate

import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set API keys (fallback to hardcoded for testing; prefer .env in production)
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY") or 'AIzaSyDc0-nLQCGSOHA2Y22RZj-YCliOO1_f6vM'
os.environ["PINECONE_API_KEY"] = os.environ.get("PINECONE_API_KEY") or "pcsk_47vyMh_QYDJNv155bd78wVoUxjUE6WNnEvW1BVKMhHBXB2LLAmdttr5DR3mF3XmBwZ4xzu"
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY") or "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"

# Function to get embeddings
def download_genAi():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return embeddings

# Load embeddings and vector store (using your existing index)
embeddings = download_genAi()
index_name = "spbot"  # Define here; matches your Pinecone setup
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Initialize LLM (fixed: use 'model' not 'model_name', no 'config', direct params)
# llm = ChatGroq(
#     groq_api_key=os.environ["GROQ_API_KEY"],
#     model="llama-3.3-70b-versatile",
#     temperature=0.8,
#     max_tokens=512
# )

llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model_name="llama-3.3-70b-versatile",
    temperature=0.8,
    max_tokens=512
)


# Prompt setup (from your prompt.py)
PROMPT = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
chain_type_kwargs = {'prompt': PROMPT}

# Create RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=docsearch.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

# Home route (renders chat.html)
@app.route('/')
def index():
    return render_template('chat.html')

# Chat endpoint (updated route to match JS fetch)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.form.get("message")  # Updated to match JS body key
        if not msg:
            return jsonify({"error": "No message provided"}), 400
        
        print("User input:", msg)
        result = qa({"query": msg})
        response_text = result["result"]
        print("Response:", response_text)
        
        return jsonify({"response": response_text})  # Return JSON to match JS expectation
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "An error occurred processing your request"}), 500

if __name__ == '__main__':
    app.run(debug=True)
