# Blur2reveal  
A full-stack FastAPI + React platform for token-based image unlocking.

Blur2reveal is a digital content platform where creators upload images with blurred previews, and users can unlock full-resolution versions using tokens. The project includes wallet logic, unlock tracking, secure access control, and a scalable architecture built for future payment integration and cloud storage.

---

## 🚀 Features

### ✔️ Current MVP
- FastAPI backend (Python)
- React frontend (Create React App)
- User registration & login (placeholder auth)
- Creator mode for adding photos
- Blurred preview gallery
- Token-based unlock system
- Demo token wallet (add 50 tokens instantly)
- Unlock history per user
- Basic access control (unlocked images stay unlocked)

### 🔜 Coming Soon
- Stripe payments for token purchases  
- PostgreSQL database (Supabase recommended)  
- Real image uploads  
- Auto-blurred preview generation  
- Secure storage (S3 / R2 / Supabase Storage)  
- JWT authentication  
- Creator dashboard (earnings, stats)  
- Deployment guides (Render, Railway, Vercel)

---

## 📁 Project Structure
---

## 🏃‍♂️ How to Run Blur2Reveal

Blur2Reveal has two parts that run together:

- **Backend:** FastAPI (Python)
- **Frontend:** React (Node.js)

Follow these steps on any Windows, macOS, or Linux computer.

---

# 🔧 1. Clone the Repository

```bash
git clone https://github.com/QueBallSharken/Blur2reveal.git
cd Blur2reveal
```

---

# 🐍 2. Run the Backend (FastAPI)

### Enter the backend folder:
```bash
cd backend
```

### Create a virtual environment:

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Start the backend server:
```bash
uvicorn main:app --reload
```

Backend will run at:
👉 http://localhost:8000

---

# ⚛️ 3. Run the Frontend (React)

Open a **second terminal window**  
(backend must stay running)

### Go to the frontend:
```bash
cd Blur2reveal/frontend
```

### Install React dependencies:
```bash
npm install
```

### Start the frontend:
```bash
npm start
```

Frontend will run at:
👉 http://localhost:3000

---

# 🎉 4. Use the App

Once both are running:

- Go to **http://localhost:3000**
- Create a test account
- Add demo tokens
- Unlock a blurred image

Your app is now running locally.

---

# 🛑 5. Stop the App

### Backend:
CTRL + C

### Frontend:
CTRL + C

---

If you want to simplify this further, see the **Docker section** below.
---

## 🐳 Running Blur2Reveal with Docker

Docker makes it easy to run the entire project (backend + frontend) without installing Python or Node.js.

### 📁 Required Files in the Repository

These files must exist:

```
backend/Dockerfile
frontend/Dockerfile
docker-compose.yml
```

They are already included in this project.

---

## 🚀 1. Build & Start Everything

From the project root:

```bash
docker compose up --build
```

This will:

- Build the FastAPI backend image  
- Build the React frontend image  
- Start both services together  

---

## 🌐 2. Access the App

Frontend (React):
👉 http://localhost:3000

Backend API (FastAPI):
👉 http://localhost:8000

API Documentation (Swagger):
👉 http://localhost:8000/docs

---

## 🛑 3. Stop the App

Press:

```
CTRL + C
```

Or use:

```bash
docker compose down
```

---

## 🧼 4. Rebuild After Code Changes

```bash
docker compose up --build
```

---

## 🐳 Why Use Docker?

- No Python or Node installation required  
- Same environment on every computer  
- Simple to run for collaborators  
- Easy to deploy later  

If you want a **production-ready Docker setup** (nginx, SSL, optimized builds), just ask.
