# AI Text Summarization Agent (Google ADK Integrated)

A production-ready, modularized FastAPI service designed for high-performance text summarization. This project utilizes the **Google Agent Development Kit (ADK)** and the **Gemini 2.0 Flash** model, featuring a robust multi-model fallback system for maximum reliability and quota resilience.

---

## 🏗 Architecture & Design (ADK-Friendly)

This project follows the **Agent Development Kit (ADK)** modular structure, separating API logic from agent execution and tool definitions.

```mermaid
graph TD
    User([User]) -->|POST /summarize| FastAPI[FastAPI Entry Point]
    FastAPI -->|Await| Agent[GeminiAgent]
    Agent -->|run_async| ADK[Google ADK Runner]
    ADK -->|Primary| G1[Gemini 2.0 Flash]
    ADK -->|Fallback 1| G2[Gemini 1.5 Flash]
    ADK -->|Fallback 2| G3[Gemini-Flash-Latest]
    ADK -->|Memory| IMS[InMemorySessionService]
    Agent -->|JSON Result| FastAPI
    FastAPI -->|200 OK| User
```

### Key Components
- **`app/main.py`**: The FastAPI application handling routing and async execution.
- **`app/agent.py`**: Core logic leveraging `google.adk.agents.Agent` and `google.adk.Runner`.
- **`app/tools.py`**: Ready-to-use module for extending agent capabilities with custom tools.
- **Multi-Model Fallback**: Automatically cycles through multiple Gemini models to bypass 429 Resource Exhausted errors.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.14+
- Google Gemini API Key ([Get it here](https://aistudio.google.com/))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/abhi542/Text_Summary_Agent_using_google_ADK.git
cd Text_Summary_Agent_using_google_ADK

# Setup Virtual Environment
python -m venv venv
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
PORT=8080
```

### 4. Running the Service
```bash
python -m app.main
```

---

## 🧪 Testing with Sample Data

### Sample Request
```bash
curl -X POST http://localhost:8080/summarize \
     -H "Content-Type: application/json" \
     -d @sample_request.json
```

### Sample Response
```json
{
  "summary": "The Eiffel Tower is a wrought-iron lattice icon in Paris, France. Named after engineer Gustave Eiffel, it served as the 1889 World's Fair centerpiece. Today, it is recognized globally as a cultural symbol of the French nation.",
  "model": "gemini-flash-latest"
}
```
<img width="1600" height="1040" alt="image" src="https://github.com/user-attachments/assets/1e6b5c79-dbba-41fe-bf8e-252d29a5cd6e" />

---

## 🐳 Docker Support
Build and run locally with Docker:
```bash
docker build -t summarizer-agent .
docker run -p 8080:8080 --env-file .env summarizer-agent
```

---

## 🛡 Security & Best Practices
- **Secret Management**: `.env` is ignored by Git to prevent API key leakage. For production, use **Google Secret Manager**.
- **Containerization**: Optimized Dockerfile f


or deployment to **Google Cloud Run**.
- **Modularity**: ADK-compliant structure ensures easy scalability and tool integration.



## Demo Video 
https://github.com/user-attachments/assets/2d5cbe27-aa0f-4a64-9e0f-792788d8ef5a

---

## 📜 Google Certification Notes
This implementation demonstrates:
- Comprehensive use of the **Google GenAI Python SDK**.
- Implementation of **Agent Development Kit (ADK)** patterns (`Runner`, `SessionService`).
- Robust error handling and model fallback strategies.
- Clean, modular, and well-documented Python code.

  
