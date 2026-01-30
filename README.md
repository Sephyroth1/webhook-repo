# webhook-repo

This repository contains the webhook receiver and UI for the GitHub Webhook
assessment task.

It is organized as a **monorepo** containing both the backend and frontend.

## Overview

The application flow is:

GitHub → Webhook (Flask) → MongoDB → API → React UI (polls every 15 seconds)

The backend receives GitHub webhook events and stores minimal required data
in MongoDB.  
The frontend polls the backend every 15 seconds and displays the latest activity.

## Repository Structure
```folder
webhook-repo/
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ └── .env.example
│
├── frontend/
│ ├── src/
│ ├── package.json
│ └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## Backend (Flask + MongoDB)

### Features

- Receives GitHub webhook events
- Handles:
  - PUSH
  - PULL_REQUEST
  - MERGE (bonus)
- Stores minimal required data in MongoDB
- Exposes `/events` API for the frontend

### Setup

1. Create a virtual environment and install dependencies:
```python
pip install -r requirements.txt
```

2. Create a `.env` file:

```.env
MONGO_URL=<your-mongodb-connection-string>
DATABASE=<database-name>
```

3. Run the Flask app:
```bash
python app.py
```

4. Expose the server using ngrok:

```bash
ngrok http 5000
```

5. Configure GitHub webhook to point to:
```bash
<ngrok-url>/webhook
```

---

## Frontend (React + Vite)

### Features

- Polls backend every 15 seconds
- Displays formatted GitHub activity:
- `{author} pushed to {branch}`
- `{author} submitted a pull request`
- `{author} merged a branch`

### Setup

1. Install dependencies:
```bash
npm install
```

2. Run the development server:

```bash
npm run dev
```

3. The frontend fetches data from:

**GET /events**


---

## API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/webhook` | Receives GitHub webhook events |
| GET  | `/events`  | Returns latest stored events |

---

## Testing

1. Push a commit to `action-repo` → PUSH event stored
2. Create a pull request → PULL_REQUEST event stored
3. Merge the pull request → MERGE event stored
4. Verify updates appear in the UI within 15 seconds

---

## Notes

- MongoDB collections are created automatically on first insert
- Webhook security can be extended using a secret (optional)
- The monorepo structure is used for convenience and clarity
