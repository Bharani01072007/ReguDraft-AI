# ReguDraft AI - FastAPI & LangGraph Backend

This is the backend service for **ReguDraft AI**, built using **FastAPI**, **LangGraph** (multi-agent orchestration), **PostgreSQL** (relational storage), **Qdrant** (vector database for RAG guidelines), and **Redis** (caching and state brokerage).

---

## 🛠️ Prerequisites

Ensure you have the following installed on your machine:
* **Python 3.10+** (Tested with Python 3.14)
* **Pip** (Python package installer)
* **Docker & Docker Compose** (Optional, for full tech stack containerization)

---

## 🚀 Quick Start - Local Running (SQLite Dev Mode)

The backend is configured to work out-of-the-box using a local SQLite database (`regudraft.db`) and mock services if external databases are not available.

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the FastAPI Server:**
   ```bash
   python main.py
   ```

5. **Access the Application API Documentation:**
   * **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   * **ReDoc UI:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🐳 Running with Docker Compose (Full Stack - Production Mode)

This launches the FastAPI application along with PostgreSQL, Redis, and Qdrant containers in an isolated local network.

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Run Docker Compose:**
   ```bash
   docker compose up --build -d
   ```

3. **Verify running containers:**
   ```bash
   docker compose ps
   ```

4. **Shutdown and Clean Volumes:**
   ```bash
   docker compose down -v
   ```

---

## 🧪 Running Automated Tests

To execute the unit tests verifying authentication, LangGraph agent routing, and the document draft review/approval lifecycle:

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Execute Pytest:**
   ```bash
   python -m pytest tests/
   ```

---

## 📂 Project Structure

```
backend/
├── main.py                     # FastAPI entrypoint
├── config.py                   # Configuration and settings loader
├── requirements.txt            # Python library dependencies
├── Dockerfile                  # Application container configuration
├── docker-compose.yml          # Container orchestration script
├── api/                        # REST API routing layer
├── auth/                       # JWT tokens and password hashing
├── database/                   # SQLAlchemy schemas and database sessions
├── schemas/                    # Pydantic validation request/response models
├── agents/                     # LangGraph states, graph, and agent nodes
├── services/                   # PDF/DOCX exporters, RAG queries, S3 helpers
└── tests/                      # Automated unit test suite
```
