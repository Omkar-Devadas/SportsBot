🏏 Sports & Health Wiki Chatbot

A conversational AI chatbot that answers sports and health-related queries by combining knowledge from:

📄 Local documents (sports/health PDFs) stored in Pinecone

🌐 Wikipedia (dynamic retrieval)

🤖 Groq LLM for generating final answers

The bot is built using Flask + LangChain + Pinecone + Google Generative AI embeddings, with a clean chat UI.




<img width="1280" height="800" alt="Screenshot 2025-08-21 at 4 09 31 PM" src="https://github.com/user-attachments/assets/46592bd2-0842-49ce-8feb-924b6f58ed5a" />
🚀 Features

🔍 Entity Extraction → Detects if a query is about a sport or person

📂 Local Knowledge Retrieval → Fetches relevant answers from your PDF documents via Pinecone

🌐 Wikipedia Integration → Retrieves additional knowledge dynamically from Wikipedia

🧠 Answer Synthesis → Combines both sources into one clear, non-repetitive response

🖥️ Web UI → Simple chat interface powered by Flask



<img width="1280" height="800" alt="Screenshot 2025-08-21 at 4 10 58 PM" src="https://github.com/user-attachments/assets/e9482a86-d14e-48a9-9720-07606bf08ef6" />

🛠️ Tech Stack

Backend: Flask (Python)

LLM: Groq’s LLaMA (via langchain_groq)

Vector Database: Pinecone (for semantic search on local docs)

Embeddings: Google Generative AI Embeddings

Document Loader: WikipediaLoader (LangChain)
