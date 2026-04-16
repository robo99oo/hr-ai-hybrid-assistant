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

Start MCP Server

python main.py

Run Hybrid AI Agent

python hybrid_agent.py

## Example Queries

## RAG Queries

What is the leave policy?
How many sick leaves are allowed?
Can I carry forward earned leave?

## MCP Actions

Apply leave for 2 days
Book sick leave
Request vacation leave

## Hybrid Queries

Can I take leave tomorrow?
Should I apply leave if I am sick?
What happens if I exceed leave limit?

## Tech Stack

. Python
FAISS (Vector Database)
LangChain
HuggingFace Transformers
Sentence Transformers
MCP (Model Context Protocol)
FastAPI / Uvicorn

Future Improvements
Replace rule-based routing with LLM-based decision system
Add FastAPI backend for API access
Build frontend UI (Streamlit or React)
Connect real HR database (SQL integration)
Deploy on cloud (AWS / Render / Railway)
Author

Kshiti Tyagi

Project Goal

To demonstrate a real-world AI HR assistant that integrates knowledge retrieval (RAG), tool execution (MCP), and intelligent routing in a single system.
