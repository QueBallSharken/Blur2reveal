# Blur2reveal: BBIS-Governed Asset Platform

A full-stack FastAPI + React platform for token-based image unlocking, integrated with **Boundary-to-Boundary Invariant Survival (BBIS)** and execution-boundary governance for secure payload delivery.

Blur2reveal serves as both a functional digital content platform and a live architectural showcase. Creators upload images with blurred previews, and users unlock full-resolution versions using tokens—governed by runtime invariant checks to ensure security context validity at the exact point of execution.

---

## 🚀 Features & Architecture

### ✔️ Current Core & Security Architecture
- FastAPI backend (Python) with **BBIS Boundary Enforcement Middleware**
- React frontend (Create React App / Vite)
- User registration & login with cryptographic session state tracking
- Creator mode for adding secured assets
- Blurred preview gallery with live invariant verification
- Token-based unlock system with execution-boundary checks
- Demo token wallet (add 50 tokens instantly)
- Unlock history per user with signed audit records

### 🔜 Coming Soon
- Stripe payments for token purchases  
- PostgreSQL database (Supabase recommended) with immutable state logging  
- Real image uploads with automated semantic validation  
- Secure storage (S3 / R2 / Supabase Storage) with cryptographic envelope validation  
- JWT & Hardware-backed token authentication  
- Creator dashboard (earnings, security telemetry, stats)  

---
