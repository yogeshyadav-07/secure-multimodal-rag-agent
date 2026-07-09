# 🔒 Secure OmniAgent Pro

An elite, multi-modal enterprise AI assistant platform secured with Supabase Identity Management. Built with Streamlit and LangChain, featuring localized interfaces in English, Hindi, and Hinglish. Anchored to a factual 2026 timeline.

👉 **Live Deployment (Hugging Face Spaces):** 
https://huggingface.co/spaces/yogesh-yadav/omni-agent-pro

---

## 🚀 Project Overview

Secure OmniAgent Pro is a highly scalable and secure multi-modal AI workstation engineered for enterprise workloads. By utilizing state-of-the-art Large Language Models (via Mistral AI), robust Vector RAG pipelines for documents, and real-time internet search capabilities, it brings actionable intelligence directly into a controlled environment.

## ✨ Core Features

### 🔐 1. Enterprise Identity & Access Management
* **Secure Gateway:** Integrated Registration and Login interface to prevent unauthenticated access.
* **Database Guardrails:** User profiles, tokens, and active sessions are persistently tracked using **Supabase RLS** (Row-Level Security).
* **Password Encryption:** Zero-knowledge compliance via robust SHA-256 password hashing.

### 🌐 2. Native Localization (Multi-Language)
The system UI elements and operational guardrails automatically shift depending on the active preference node:
* **English:** Corporate/Standard operational language.
* **Hindi (हिन्दी):** Complete vernacular dev translation.
* **Hinglish:** Hybrid interaction layer optimized for colloquial enterprise team communication.

### 🧠 3. Advanced Multi-Modal Context Engine
The system analyzes user input and dynamically routes instructions across dedicated background engines:
* **🧬 Core LLM Brain:** Deep contextual reasoning powered by `mistral-large-latest`.
* **🖼️ Computer Vision Node:** Accepts heavy file buffers (PNG, JPG, JPEG) to run real-time optical/structural analysis.
* **📄 Document Vector Index (RAG):** Implements dynamic in-memory **ChromaDB** parsing with `HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`) to query raw PDF schemas.
* **🌐 Live Web Search Engine (Tavily):** Automatic external context retrieval if queries demand ultra-recent or 2026 chronological facts.

---

## 🛠️ Tech Stack & Dependencies

* **Frontend Engine:** Streamlit (v1.35.0+)
* **AI Orchestration:** LangChain / LangChain Core / LangChain Community
* **Base Framework Model:** Mistral AI API Layer
* **Vector VectorDB:** ChromaDB
* **Data Storage / Auth:** Supabase Client Engine
* **Context Fetcher:** Tavily Search Engine

---

## ⚙️ Local Configuration & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yogeshyadav-07/secure-multimodal-rag-agent.git
cd secure-multimodal-rag-agent
2. Environment Variables (.env)
Create a .env file in the root structure of your directory and insert your secure API tokens:

Code snippet
MISTRAL_API_KEY=your_mistral_api_token
TAVILY_API_KEY=your_tavily_search_token
SUPABASE_URL=your_supabase_project_endpoint
SUPABASE_KEY=your_supabase_anon_public_key
3. Database Schema Blueprint
Execute the following SQL commands inside the Supabase SQL Editor to construct the target data node:

SQL
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT timezone('utc'::text, now()) NOT NULL
);
4. Running the Local Server
Bash
pip install -r requirements.txt
streamlit run app.py
🤗 Hugging Face Spaces Deployment Workflow
Since this repository is configured for cloud synchronization, you can easily host it on Hugging Face Spaces:

Space Creation: Create a new Space on Hugging Face and choose Streamlit as the SDK.

Repository Sync: Push this codebase directly to your Hugging Face Space Git remote endpoint.

Important Note on Secrets: Go to the Space Settings -> Variables and secrets tab and add the following securely:

MISTRAL_API_KEY

TAVILY_API_KEY

SUPABASE_URL

SUPABASE_KEY

3. Database Schema Blueprint
Execute the following SQL commands inside the Supabase SQL Editor to construct the target data node:

SQL
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT timezone('utc'::text, now()) NOT NULL
);
4. Running the Local Server

Bash
pip install -r requirements.txt
streamlit run app.py
