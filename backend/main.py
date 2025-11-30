from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

app = FastAPI()

# --- CORS (allows React frontend to connect) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "database"
users_db = {}
photos_db = {}
unlocks_db = []
token_transactions_db = []

# Models
class UserCreate(BaseModel):
    email: str
    password: str
    is_creator: bool = False

class UserPublic(BaseModel):
    id: str
    email: str
    is_creator: bool
    token_balance: int

class PhotoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price_tokens: int
    preview_url: str
    original_url: str

class PhotoPublic(BaseModel):
    id: str
    creator_id: str
    title: str
    description: Optional[str]
    price_tokens: int
    preview_url: str
    unlocked: bool = False

class UnlockRequest(BaseModel):
    photo_id: str

class TokenPurchaseRequest(BaseModel):
    amount: int

# Fake auth
def get_current_user(user_id: str):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user

# Auth routes
@app.post("/auth/register", response_model=UserPublic)
def register(user_in: UserCreate):
    for u in users_db.values():
        if u["email"] == user_in.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid4())
    users_db[user_id] = {
        "id": user_id,
        "email": user_in.email,
        "password": user_in.password,
        "is_creator": user_in.is_creator,
        "token_balance": 0,
        "created_at": datetime.utcnow(),
    }
    return UserPublic(
        id=user_id,
        email=user_in.email,
        is_creator=user_in.is_creator,
        token_balance=0,
    )

@app.post("/auth/login", response_model=UserPublic)
def login(email: str, password: str):
    for user in users_db.values():
        if user["email"] == email and user["password"] == password:
            return UserPublic(
                id=user["id"],
                email=user["email"],
                is_creator=user["is_creator"],
                token_balance=user["token_balance"],
            )
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Photo routes
@app.post("/photos", response_model=PhotoPublic)
def create_photo(photo_in: PhotoCreate, user_id: str):
    user = get_current_user(user_id)
    if not user["is_creator"]:
        raise HTTPException(status_code=403, detail="Only creators can upload")

    photo_id = str(uuid4())
    photos_db[photo_id] = {
        "id": photo_id,
        "creator_id": user["id"],
        "title": photo_in.title,
        "description": photo_in.description,
        "price_tokens": photo_in.price_tokens,
        "preview_url": photo_in.preview_url,
        "original_url": photo_in.original_url,
        "created_at": datetime.utcnow(),
    }
    return PhotoPublic(
        id=photo_id,
        creator_id=user["id"],
        title=photo_in.title,
        description=photo_in.description,
        price_tokens=photo_in.price_tokens,
        preview_url=photo_in.preview_url,
        unlocked=False,
    )

@app.get("/photos", response_model=List[PhotoPublic])
def list_photos(user_id: Optional[str] = None):
    unlocked = {r["photo_id"] for r in unlocks_db if r["user_id"] == user_id}
    output = []
    for p in photos_db.values():
        output.append(
            PhotoPublic(
                id=p["id"],
                creator_id=p["creator_id"],
                title=p["title"],
                description=p["description"],
                price_tokens=p["price_tokens"],
                preview_url=p["preview_url"],
                unlocked=p["id"] in unlocked,
            )
        )
    return output

@app.get("/photos/{photo_id}")
def get_photo(photo_id: str, user_id: str):
    user = get_current_user(user_id)
    photo = photos_db.get(photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Not found")

    unlocked = any(
        r["user_id"] == user["id"] and r["photo_id"] == photo_id
        for r in unlocks_db
    )

    if unlocked:
        return {
            "id": photo["id"],
            "title": photo["title"],
            "description": photo["description"],
            "original_url": photo["original_url"],
            "price_tokens": photo["price_tokens"],
            "unlocked": True,
        }
    else:
        return {
            "id": photo["id"],
            "title": photo["title"],
            "description": photo["description"],
            "preview_url": photo["preview_url"],
            "price_tokens": photo["price_tokens"],
            "unlocked": False,
        }

# Wallet
@app.get("/wallet", response_model=int)
def get_wallet(user_id: str):
    user = get_current_user(user_id)
    return user["token_balance"]

@app.post("/wallet/add")
def add_tokens(req: TokenPurchaseRequest, user_id: str):
    user = get_current_user(user_id)
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    user["token_balance"] += req.amount
    return {"token_balance": user["token_balance"]}

# Unlock
@app.post("/unlock")
def unlock_photo(req: UnlockRequest, user_id: str):
    user = get_current_user(user_id)
    photo = photos_db.get(req.photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Already unlocked?
    if any(
        r["user_id"] == user["id"] and r["photo_id"] == req.photo_id
        for r in unlocks_db
    ):
        return {"detail": "Already unlocked", "token_balance": user["token_balance"]}

    price = photo["price_tokens"]
    if user["token_balance"] < price:
        raise HTTPException(status_code=400, detail="Not enough tokens")

    user["token_balance"] -= price
    unlocks_db.append(
        {
            "id": str(uuid4()),
            "user_id": user["id"],
            "photo_id": req.photo_id,
            "tokens_spent": price,
            "created_at": datetime.utcnow(),
        }
    )
    return {"detail": "Unlocked", "token_balance": user["token_balance"]}
