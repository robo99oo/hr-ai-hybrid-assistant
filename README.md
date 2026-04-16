## HR AI Hybrid Assistant (RAG + MCP + AI Agent)

An AI-powered HR assistant system that combines Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP) tools, and a hybrid routing engine to handle HR policy queries and automate HR actions like leave management.

## Features
1. RAG-based HR Knowledge System
2. Answers HR policy-related questions
3. Uses FAISS vector database for semantic search
4. Powered by HuggingFace sentence-transformer embeddings
5. Efficient retrieval of HR rules and guidelines

## MCP Tool Integration
1. Executes HR-related actions programmatically
2. Supports leave application workflow
3. Simulates HR system operations using tools

## Hybrid AI Router

Routes user queries intelligently into:

1. RAG for policy and knowledge-based queries
2. MCP for action-based requests
3. Hybrid mode for combined reasoning and suggestions

## AI Decision Flow
The system decides:

1. What the user is asking
2. Which subsystem to use
3. How to generate the final response

## Architecture
User Query
→ Hybrid AI Router
→ RAG Pipeline (FAISS + Embeddings) OR MCP Tools OR LLM Response
→ Final Response

## Project Structure

## hr-ai-hybrid-assistant/

RAG.py # HR policy knowledge base + vector search
hybrid_agent.py # AI routing engine
main.py # MCP server (HR tools)
app.py # optional runner
requirements.txt # dependencies
README.md

Installation
1. Clone repository

git clone https://github.com/your-username/hr-ai-hybrid-assistant.git

cd hr-ai-hybrid-assistant

2. Create virtual environment

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

## Required Packages

1. pip install langchain
2. pip install langchain-community
3. pip install langchain-huggingface
4. pip install langchain-text-splitters
5. pip install faiss-cpu
6. pip install sentence-transformers
7. pip install fastapi
8. pip install uvicorn

## How to Run

1. Start MCP Server

2. python main.py

3. Run Hybrid AI Agent

4. python hybrid_agent.py

## Example Queries

## RAG Queries

1. What is the leave policy?
2. How many sick leaves are allowed?
3. Can I carry forward earned leave?

## MCP Actions

1. Apply leave for 2 days
2. Book sick leave
3. Request vacation leave

## Hybrid Queries

1. Can I take leave tomorrow?
2. Should I apply leave if I am sick?
3. What happens if I exceed leave limit?

## Tech Stack

1. Python
2. FAISS (Vector Database)
3. LangChain
4. HuggingFace Transformers
5. Sentence Transformers
6. MCP (Model Context Protocol)
7. FastAPI / Uvicorn

## Future Improvements
1. Replace rule-based routing with LLM-based decision system
2. Add FastAPI backend for API access
3. Build frontend UI (Streamlit or React)
4. Connect real HR database (SQL integration)
5. Deploy on cloud (AWS / Render / Railway)
   
## Author
Kshiti Tyagi

## Project Goal

To demonstrate a real-world AI HR assistant that integrates knowledge retrieval (RAG), tool execution (MCP), and intelligent routing in a single system.



<img width="1456" height="1024" alt="image" src="https://github.com/user-attachments/assets/fb999ac4-7c4f-4b03-bc36-d1bf64018d60" />
