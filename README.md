# 🌿 GreenPath

**GreenPath** is a sustainability tracking web app that helps users monitor and reduce their carbon footprint.  
Users can log eco-friendly activities, track emission data, and receive AI-powered insights to live more sustainably.

---

## 🚀 Live Links

- **Frontend (Vercel):** [https://green-path-pearl.vercel.app](https://green-path-pearl.vercel.app)  
- **Backend (Render):** [https://green-path.onrender.com](https://green-path.onrender.com)

---

## 🧩 Tech Stack

### Frontend
- **React.js (Vite)**
- **Firebase Authentication**
- **CSS3 / Tailwind**
- **Deployed on Vercel**

### Backend
- **Flask (Python)**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **Flask-CORS**
- **Google Generative AI**
- **Deployed on Render**

---

## ⚙️ Project Structure

Green-Path/
│
├── backend/ # Flask backend
│ ├── app.py # App entry point
│ ├── models.py # Database models
│ ├── routes/ # API routes (e.g., AI, activities, community)
│ ├── controllers/ # Business logic
│ ├── services/ # AI integrations and helpers
│ ├── db/ # Database setup
│ ├── migrations/ # Alembic migration files
│ ├── config.py # Environment configuration
│ ├── requirements.txt # Backend dependencies
│ └── Procfile # Render process command
│
├── frontend/ # React frontend
│ ├── src/ # React components and pages
│ ├── public/ # Static files
│ ├── package.json # Frontend dependencies
│ └── vite.config.js # Vite configuration
│
├── runtime.txt # Python runtime version for Render
├── requirements.txt # Root-level requirements for Render
└── README.md # This file

yaml
Copy code

---

## 🧠 Features

✅ Log daily activities and view total emissions  
✅ View AI-powered sustainability insights  
✅ Visualize your weekly carbon data  
✅ Participate in the community section  
✅ Authentication and user-based activity logging  

---

## 🌍 Deployment Configuration

### 🔹 Backend (Render)
1. **Root setup**
   - Place `requirements.txt` and `runtime.txt` in the project root.
   - Set **Start Command** in Render to:
     ```
     cd backend && python app.py
     ```

2. **CORS setup (app.py)**
   ```python
   from flask_cors import CORS

   CORS(app, resources={
       r"/api/*": {
           "origins": [
               "http://localhost:5173",
               "http://127.0.0.1:5173",
               "https://green-path-pearl.vercel.app"
           ]
       }
   }, supports_credentials=True)
Environment Variables


🔹 Frontend (Vercel)
Base URL Configuration

Replace all local API URLs (e.g., http://127.0.0.1:5000) with:

https://green-path.onrender.com

Build Settings

Framework: Vite (React)

Build Command: npm run build

Output Directory: dist

🧪 Local Development
Backend
bash
Copy code
cd backend
pip install -r requirements.txt
python app.py
Frontend
bash
Copy code
cd frontend
npm install
npm run dev
Then open http://localhost:5173

🧰 Environment Variables
Backend (.env or Render)
ini
Copy code
GOOGLE_API_KEY=your_google_api_key
FLASK_ENV=development
DATABASE_URL=sqlite:///db.sqlite3
Frontend (.env or Vercel)
ini
Copy code
VITE_API_BASE_URL=https://green-path.onrender.com
VITE_FIREBASE_API_KEY=your_firebase_key


👥 Collaborators
Name	Role
Ernest Munyoki	Full-Stack Developer
Fred Mwangi	Backend Developer
Mary Nyarangi	Frontend Developer


🪴 License
This project is licensed under the MIT License — feel free to use and improve it.

"Small actions make a big impact — start your green path today." 🌱

---










