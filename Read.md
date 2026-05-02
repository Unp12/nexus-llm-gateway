# 🌐 Nexus LLM Gateway

A high-performance, asynchronous middleware gateway designed to intelligently route, manage, and execute prompts across multiple Large Language Models (LLMs) including Google Gemini, OpenAI, and Anthropic Claude.

<img width="947" height="434" alt="image" src="https://github.com/user-attachments/assets/250b2a98-f74a-4008-840c-895aa08e5a7a" />


## 🚀 The Engineering Challenge

In today's AI landscape, relying on a single LLM provider exposes applications to rate limits (HTTP 429), server downtime (HTTP 503), and unpredictable latency. Furthermore, heavy reliance on abstraction frameworks (like LangChain) can obscure underlying network inefficiencies.

**The Nexus LLM Gateway solves this by implementing a custom, raw HTTP routing engine.** 

Instead of wrapping APIs, this project uses native asynchronous Python to manage connection pools, enforce strict timeouts, and implement automatic provider fallbacks. This ensures 99.9% uptime for AI requests by seamlessly routing traffic to a secondary model if the primary engine fails.

## ✨ Core Features

*   **⚡ Async Processing:** Built with FastAPI and `httpx` for non-blocking, highly concurrent API execution.
*   **🛡️ Resilient Routing (Primary-Fallback):** Automatically catches HTTP timeouts or rate limits and silently routes the prompt to a secondary provider without interrupting the user experience.
*   **⏱️ Latency Tracking:** Calculates and logs exact millisecond execution times to monitor provider health and performance.
*   **🔌 Zero-Bloat Architecture:** Uses raw HTTPS REST calls instead of heavy, constantly-breaking wrapper libraries.
*   **🎨 Production UI:** A clean, responsive React frontend (built with Vite) that displays routing metrics and system states in real-time.

## 🏗️ System Architecture

```text
[ React Client ] 
       │ (JSON Payload: Prompt + Primary Engine)
       ▼
[ FastAPI Server ] ──► [ Async Resilient Router ]
                               │
            ┌──────────────────┴──────────────────┐
     (Success < 15s)                       (Timeout / HTTP 429)
            ▼                                     ▼
[ Primary Engine ]                        [ Fallback Engine ]
  (e.g., Gemini)                            (e.g., OpenAI)
            │                                     │
            └──────────────────┬──────────────────┘
                               ▼
                    [ Standardized Response ]
                     (Text + Latency Metrics)
🛠️ Tech Stack
Backend: Python 3.12, FastAPI, Uvicorn, httpx, asyncio

Frontend: React, Vite, raw CSS for styling

Concepts: MLOps, API Gateway Pattern, Fault Tolerance, RESTful Networking

🚦 Local Setup & Installation
1. Clone the Repository
Bash
git clone https://github.com/Unp12/nexus-llm-gateway.git
cd nexus-llm-gateway
2. Backend Setup
Navigate to the backend directory and set up your virtual environment:

Bash
cd backend
python -m venv venv

# Windows:
.\venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
Environment Variables:
Create a .env file in the backend/ root:

Code snippet
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here # Optional
Run the Server:

Bash
python -m uvicorn app.main:app --reload
The backend will run on [http://127.0.0.1:8000](http://127.0.0.1:8000). Swagger docs available at /docs.

3. Frontend Setup
Open a new terminal window and navigate to the frontend directory:

Bash
cd frontend
npm install
npm run dev
The application will be available at http://localhost:5173
