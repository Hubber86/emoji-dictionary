# ​ Emoji Dictionary

A polished full-stack web application that enables seamless storage, lookup, and management of emojis based on words. Built with a modern stack using **FastAPI (backend)**, **PostgreSQL (database)**, and **React + Vite (frontend)**.

---

##  Live Preview  
View the deployed app on [Render](https://render.com) — includes auto-deployed backend and frontend.

---

##  Features
- **Search** emojis by word (e.g., “cat” → 🐱)
- **Add & Update** emoji-word mappings via a RESTful API
- **Clean UI** built with React, offering real-time search and display
- **Schema-managed PostgreSQL** for reliable, scalable storage
- **One-click deployment** with Render (free tier supported)

---

##  Project Structure

emoji-dictionary/
│
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ └── .render.yaml
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx
│ │ └── index.jsx
│ ├── package.json
│ ├── vite.config.js
│ └── .render.yaml
│
└── db/
└── schema.sql

---

##  Technology Stack

- **Backend:** Python | FastAPI, Uvicorn  
- **Database:** PostgreSQL (managed via Render)  
- **Frontend:** React, Vite  
- **Deployment:** Render (CI/CD enabled)

---

##  Why This Project Matters

- **Interactive Emoji Dictionary:** Great for educators, language learners, and UI designers.  
- **Integration-Ready:** Easily plug into messaging apps or learning platforms.  
- **SaaS Potential:** Build on top for commercial use — paid API access, premium features, or enterprise plugins.

---

##  Getting Started

1. **Clone the repo**  
   ```
   git clone https://github.com/Hubber86/emoji-dictionary.git
Deploy to Render — follow the .render.yaml configurations in both frontend and backend.

Initialize the Database
psql $DATABASE_URL -f db/schema.sql
Visit your sites:

Frontend: https://emoji-frontend.onrender.com

Backend API: https://emoji-backend.onrender.com/emoji?word=cat

##  Contribute & Collaborate
Interested in new features, partnerships, or building upon this stack? I’d love to collaborate. Feel free to open issues or pull requests!

