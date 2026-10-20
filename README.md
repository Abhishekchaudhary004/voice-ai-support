# AITLAS Voice AI Support 🎙️

An AI-powered voice customer support application for AITLAS, designed to provide an interactive support experience through a modern web interface, FastAPI backend, and ElevenLabs Conversational AI.

## ✨ Overview

AITLAS Voice AI Support combines web technologies and conversational AI to help users interact with an AI customer support assistant using voice.

The project separates the frontend and backend into independent components while keeping the source code in a single GitHub repository.

## 🚀 Features

- 🎙️ Voice-based customer interaction using ElevenLabs Conversational AI
- 💬 Interactive web interface built with React and Vite
- ⚡ REST API backend powered by FastAPI
- 🐍 Python-based backend architecture
- 🗄️ SQLite database integration for local development
- 📱 Modern, responsive frontend
- 🔐 Environment-based configuration for sensitive credentials
- 🌐 Deployment-ready repository structure

## 🛠️ Tech Stack

| Component | Technologies |
|---|---|
| Frontend | React.js, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn |
| Voice AI | ElevenLabs Conversational AI |
| Database | SQLite, SQLAlchemy |
| Version Control | Git, GitHub |
| Frontend Deployment | Vercel |
| Backend Deployment | Vercel-compatible Python deployment configuration |

## 📁 Project Structure

```text
voice-ai-support/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   └── models.py
│   ├── requirements.txt
│   └── .env                  # Local secrets; not committed
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

*Note: The structure above highlights the main components. Refer to the repository for the complete file structure.*

## ⚙️ Prerequisites

Install the following before running the project locally:

- Python 3.11 or another Python version compatible with the project's dependencies
- Node.js and npm
- Git
- An ElevenLabs account and appropriately configured voice agent

## 💻 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Abhishekchaudhary004/voice-ai-support.git
cd voice-ai-support
```

### 2. Set up the backend

Open a terminal in the project root.

Create a Python virtual environment if one does not already exist:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

Create a local `backend/.env` file containing the environment variables required by your backend and voice integration.

Use the variable names referenced by the application code. Never commit API keys, passwords, tokens, or other secrets to GitHub.

### 4. Run the backend

From the project root, run:

```powershell
cd backend
..\ .venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

If your virtual environment is already activated from the project root, you can instead run:

```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Open the API documentation at:

http://localhost:8000/docs

### 5. Set up the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL displayed by Vite in the terminal, usually:

http://localhost:5173

## 🌐 Deployment

The frontend and backend can be configured as separate Vercel projects connected to the same GitHub repository.

### Frontend

- Framework: Vite
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`

### Backend

- Root directory: `backend`
- Runtime: Python / FastAPI
- Start command and environment configuration must match the deployed backend implementation.

Configure the frontend's API base URL to point to the deployed backend. If the application uses a `VITE_` environment variable, remember that its value is visible to browser users. Never put private API keys in frontend environment variables.

Configure FastAPI CORS to allow the deployed frontend origin.

**Production note:** Local SQLite storage is not automatically persistent on every hosting platform. Use an appropriate persistent storage solution or managed database for production data.

## 🔐 Security

- Keep `.env` files out of version control.
- Never expose API keys or secret tokens in frontend code.
- Use environment settings provided by your hosting platform for backend secrets.
- Rotate credentials immediately if they are exposed.
- Restrict CORS to trusted origins.
- Avoid storing sensitive customer information unless necessary and appropriately protected.

## 🧪 Testing Checklist

- [ ] Frontend starts successfully.
- [ ] Backend starts successfully.
- [ ] API documentation is accessible.
- [ ] Frontend can communicate with the backend.
- [ ] Voice agent loads and responds.
- [ ] CORS is configured correctly.
- [ ] Production environment variables are configured securely.

## 🔮 Future Enhancements

- Persistent production database
- Customer enquiry and ticket management
- Conversation history and analytics
- Multilingual voice support
- Human support escalation
- Authentication and role-based access
- Monitoring, logging, and error reporting

## 👨‍💻 Maintainer

**AITLAS Voice AI Support**

Repository: [voice-ai-support](https://github.com/Abhishekchaudhary004/voice-ai-support)

Company website: [https://aitlas.us/](https://aitlas.us/)

---

*Built with React, FastAPI, and conversational AI technologies.*
