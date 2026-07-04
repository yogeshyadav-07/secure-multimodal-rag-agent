# 🔒 OmniAgent Pro: Secure Multi-Modal Enterprise AI Platform

OmniAgent Pro is a production-ready AI Agentic platform built using **Streamlit**, **LangChain**, and **Mistral AI**. It features an encrypted **MySQL-backed Authentication Gateway** running on a custom port, real-time web intelligence via **Tavily Search**, local document vectorization (RAG), computer vision capabilities, and a fully dynamic **Multi-Language Interface Engine** (supporting English, Hindi, and Hinglish).

---

## 🚀 Key Features

*   **🔒 Secure MySQL Auth Gateway:** Fully integrated login, signup, and user validation pipeline using `SHA-256` password hashing. Tracks user sessions safely with customizable database ports (Default: `3300`) and supports dual login via Username or Email.
*   **🌐 Tri-Lingual Localization:** Real-time UI and System engine translation. Switch seamlessly between **English**, **Hindi (हिन्दी)**, and **Hinglish** mid-session without losing chat state.
*   **🧬 Advanced Multi-Modal Architecture:**
    *   **Document RAG Index:** Dynamically chunks and vectorizes multi-page PDFs using `ChromaDB` and `HuggingFace Embeddings` (`all-MiniLM-L6-v2`) for local context injection.
    *   **Computer Vision Engine:** Converts incoming visual attachments to Base64 payloads for direct multimodal analysis using `mistral-large-latest`.
*   **🌍 Live Web Grounding (Tavily):** Detects time-sensitive or real-time intent dynamically, querying the live web to anchor answers accurately in the current temporal frame (**2026**).
*   **🌙 Dynamic Workspace Toggling:** Full dark/light mode workspace stylesheet rendering managed directly within the user session state.
*   **⚡ Real-Time Word Streaming:** Outputs responses word-by-word instantly to eliminate interface lag and reduce token load wait-times.

---

## 🛠️ Tech Stack

*   **Frontend/UI:** Streamlit (Custom Native CSS Injection)
*   **Orchestration Framework:** LangChain Core, LangChain Community
*   **LLM Provider:** Mistral AI (`mistral-large-latest` Streaming Node)
*   **Vector Database:** ChromaDB (In-Memory Processing)
*   **Embeddings Model:** HuggingFace Transformers (`all-MiniLM-L6-v2`)
*   **Database Infrastructure:** MySQL Server (Port: 3300)

---

## 📋 Prerequisites & Installation

### 1. Database Configuration
Before booting up the interface, establish the relational tracking schema in your MySQL environment (Ensure your database instance is running on port `3300` or adjust the environment variables accordingly):

```sql
CREATE DATABASE IF NOT EXISTS omni_agent_db;
USE omni_agent_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

### 2. Install Dependencies

Clone the repository and install the verified architectural packages:

```bash
pip install streamlit langchain-core langchain-community langchain-mistralai mysql-connector-python python-dotenv chromadb sentence-transformers pypdf pillow

```

### 3. Environment Variables Setup

Create a `.env` file in the root directory of your project and populate it with your operational configurations:

```env
# AI Model Infrastructure
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_search_api_key_here

# MySQL Storage Infrastructure
MYSQL_HOST=localhost
MYSQL_PORT=port_number
MYSQL_USER=root
MYSQL_PASSWORD=your_database_password_here
MYSQL_DB=omni_agent_db

```

---

## 🏎️ Running the Platform

To initialize the secure workspace gateway, execute the following execution block in your terminal:

```bash
streamlit run OmniAgent_Final.py

```

---

## 🛡️ Production Deployment Guidelines

When deploying this multi-modal agent platform to cloud nodes (e.g., HuggingFace Spaces, Streamlit Cloud, Railway, or Render):

1. Ensure that your local `.env` file is explicitly declared inside your `.gitignore` profile to avoid leaking critical API credentials.
2. Inject your production environment variables securely via the hosting provider's **Secrets / Environment Variables** management dashboard.
3. Replace the local in-memory Chroma instance with a hosted persistent solution (`Pinecone`, `Qdrant`, or `Chroma Cloud`) for long-term production state preservation.

```

```
