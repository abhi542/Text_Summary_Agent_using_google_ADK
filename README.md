# Simple Text Summariser Agent

A minimal, production-ready AI agent service that summarizes text using Google Gemini.

## Tech Stack
- **Python 3.10+** (tested on 3.14)
- **FastAPI**: High-performance web framework.
- **Google GenAI SDK**: Latest official Gemini API integration.
- **Docker**: For seamless containerization and deployment.

## Project Structure (ADK-Friendly)
```text
.
├── app/
│   ├── main.py        # FastAPI Entry Point
│   ├── agent.py       # AI Agent Logic (Gemini Fallback)
│   └── tools.py       # (Optional) Custom Tools Placeholder
├── requirements.txt   # Dependencies
├── Dockerfile          # Container Configuration
├── .dockerignore      # Files to exclude from Docker
├── .env               # Environment Variables (Local)
└── README.md          # Project Documentation
```

## Setup & Local Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   PORT=8080
   ```

3. **Run the Server**:
   ```bash
   python -m app.main
   ```

## Usage

### 1. Health Check
`GET http://localhost:8080/`

### 2. Summarize Text
`POST http://localhost:8080/summarize`

**Body (JSON):**
```json
{
  "text": "Your long text goes here..."
}
```

## Deployment to Google Cloud Run

1. **Build and Tag Image**:
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT-ID]/summariser-agent
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy summariser-agent \
     --image gcr.io/[PROJECT-ID]/summariser-agent \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY=[YOUR-KEY],PORT=8080
   ```
