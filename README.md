# 🚀 Order-to-Cash Graph Conversational Chatbot

An interactive graph-based analytics system that allows users to explore Order-to-Cash (O2C) business processes using natural language queries.

This project combines **Graph Modeling + Visualization + Conversational AI** to deliver insights from structured enterprise data.

---

## 🔥 Live Demo

- 🌐 Frontend: https://your-app.vercel.app  
- ⚙️ Backend API: https://your-app.onrender.com  

---

## 📌 Features

### 1. Graph Construction
- Built a graph from structured business datasets
- Nodes represent entities:
  - Customers
  - Sales Orders
  - Deliveries
  - Billing Documents
  - Journal Entries
- Edges represent relationships:
  - Order → Delivery
  - Delivery → Billing
  - Billing → Journal Entry

---

### 2. Graph Visualization
- Interactive force-directed graph (React)
- Features:
  - Zoom & pan
  - Node highlighting
  - Hover tooltips
  - Click-based node details
  - Relationship arrows

---

### 3. Conversational Query Interface
- Chat interface to query graph using natural language
- Converts user queries into graph traversal logic
- Highlights relevant nodes and relationships

---

### 4. Example Queries

You can ask:

- "Trace flow of order 740508"
- "Find journal entry for billing document 9115087"
- "Show broken flows in the system"

---

### 5. Guardrails
- Restricts queries to domain-specific topics
- Rejects unrelated questions

Example:
> "This system is designed to answer dataset-related questions only."

---

## 🧠 Architecture
Frontend (React + Vite)
↓
Backend (FastAPI)
↓
Graph Engine (Python)


---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- react-force-graph

### Backend
- FastAPI
- Python
- Pandas

### Deployment
- Frontend: Vercel (Free)
- Backend: Render (Free)

---

## 📂 Project Structure

---

## 🛠️ Tech Stack

### Frontend
- React.js
- Vite
- react-force-graph

### Backend
- FastAPI
- Python
- Pandas

### Deployment
- Frontend: Vercel (Free)
- Backend: Render (Free)

---

## 📂 Project Structure
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── graph.py
│ │ │ ├── query.py
│ │ │
│ │ ├── services/
│ │ │ ├── graph_builder.py
│ │ │ ├── query_engine.py
│ │ │
│ │ ├── utils/
│ │ │ ├── loader.py
│ │ │
│ │ ├── main.py
│ │
│ ├── data/
│ ├── requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── GraphView.jsx
│ │ │ ├── ChatBox.jsx
│ │ │
│ │ ├── services/
│ │ │ ├── api.js
│ │ │
│ │ ├── App.jsx
│
├── README.md

## ⚙️ Setup Instructions

### 🔹 Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend
cd frontend
npm install
npm run dev

App runs at:

http://localhost:5173