# 🚀 AI Document Intelligence Platform

## 📌 Overview

This project is a **backend-heavy AI data platform** that allows users to upload documents, process them through a data pipeline, extract insights using AI, and interact with the content via semantic search and Q&A.

It follows a real-world architecture combining:

* FastAPI (backend)
* React (frontend)
* PostgreSQL (database)
* FAISS (vector search)
* LLM integration (Ollama/OpenAI)
* Linux-based deployment (Nginx, cron, logging)

---

## 🧠 Core Features

* 📄 Upload documents (TXT/PDF/DOCX)
* 🧹 Extract and clean text
* ✂️ Split into chunks
* 🤖 Generate embeddings
* 🔍 Semantic search
* 💬 Ask questions (RAG pipeline)
* 📊 Dashboard with system stats
* 🗂 Query history tracking
* 🧾 Logging and monitoring
* ⏱ Automated cleanup using cron

---

## 🏗 System Architecture

```
User (Browser)
      ↓
Frontend (React - Vercel)
      ↓
Nginx (Reverse Proxy)
      ↓
Backend (FastAPI - Render/Linux)
      ↓
 ├── PostgreSQL (structured data)
 ├── FAISS (vector search)
 └── LLM (Ollama/OpenAI)
```

---

## ⚙️ Data Flow

```
Upload → Extract → Chunk → Store → Embed → Search → Answer
```

1. User uploads document
2. Backend extracts text
3. Text is split into chunks
4. Chunks stored in DB
5. Embeddings generated (FAISS)
6. User query → semantic search
7. LLM generates final answer

---

## 🐧 Why Linux?

This project is designed around **Linux-based execution**, which is critical for real-world backend systems.

### Benefits:

* 🔧 Better process control (services, scripts)
* ⚡ High performance and stability
* 🧠 Native support for automation (cron jobs)
* 🔐 Fine-grained file permissions
* 📂 Standardized directory structure
* 🚀 Industry-standard deployment environment

---

## 📁 Linux Directory Structure

```
/opt/app/
├── backend/
├── frontend/
├── uploads/
├── logs/
└── scripts/
```

---

## 🔄 Nginx Integration (Frontend + Backend)

Nginx acts as a **reverse proxy**, providing a single entry point.

### Flow:

```
Browser → Nginx → Backend / Frontend
```

### Routing:

* `/` → React frontend (static build)
* `/api/` → FastAPI backend

### Example Config:

```nginx
server {
    listen 80;

    location / {
        root /opt/app/frontend/dist;
        index index.html;
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
    }
}
```

### Benefits:

* Single URL for entire app
* Improved security
* Better performance
* Production-ready architecture

---

## 🤖 LLM Integration

The system uses **Retrieval-Augmented Generation (RAG)**.

### Flow:

```
User Query → Embedding → FAISS Search → Context → LLM → Answer
```

### Components:

* Embedding Model → sentence-transformers
* Vector Store → FAISS
* LLM → Ollama (local) or OpenAI (cloud)

### Why RAG?

* Reduces hallucination
* Uses real document data
* Scalable and efficient

---

## 📊 Database Tables

| Table              | Purpose              |
| ------------------ | -------------------- |
| uploaded_documents | Store uploaded files |
| document_chunks    | Store text chunks    |
| query_history      | Store user queries   |
| pipeline_logs      | Track processing     |

---

## 🔌 API Endpoints

### 📤 Upload

```
POST /upload
```

### ⚙️ Process Document

```
POST /process/{doc_id}
```

### 🧠 Generate Embeddings

```
POST /embed/{doc_id}
```

### 🔍 Semantic Search

```
POST /search
```

### 💬 Ask Question

```
POST /ask
```

### 📊 Dashboard

```
GET /dashboard
```

---

## 🧾 Logging

Logs are stored in:

```
/opt/app/logs/app.log
```

Tracks:

* uploads
* processing
* queries
* errors

---

## ⏱ Cron Job (Automation)

Automated cleanup script:

```bash
/opt/app/scripts/cleanup.sh
```

Runs daily:

```
0 2 * * * /opt/app/scripts/cleanup.sh
```

Deletes old files and maintains storage.

---

## 🧪 Testing

Basic testing is implemented using:

```
pytest
```

---

## 🔄 CI/CD Pipeline

GitHub Actions pipeline:

* Install dependencies
* Run tests
* Build frontend

---

## 🚀 Deployment

### 🐳 Docker (Backend + Postgres)

Run the backend and database locally or on a server:

```bash
docker compose up --build -d
```

Environment options:

* `AWS_REGION` (default `us-east-1`).
* `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (required for Bedrock).
* `AWS_SESSION_TOKEN` (optional, if using temporary creds).

### Frontend:

* Vercel

### Backend:

* Render

### Database:

* PostgreSQL (Render / external)

---

## 🎯 Key Highlights

* Full AI pipeline (RAG)
* Linux-based deployment
* Reverse proxy architecture
* Scalable backend design
* Real-world system integration

---

## 📌 Future Improvements

* Chat-style UI
* Streaming responses
* Role-based access
* Advanced analytics dashboard
* Multi-document comparison

---

