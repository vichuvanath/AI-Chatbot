from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
try:
    from .database import init_db, get_user, add_user
except ImportError:
    from database import init_db, get_user, add_user

app = FastAPI()

# Initialize the database on startup
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

class ChatRequest(BaseModel):
    message: str

class AuthRequest(BaseModel):
    email: str
    password: str

@app.post("/chat")
async def chat(request: ChatRequest):
    return {"response": f"You said: {request.message}"}

@app.post("/register")
async def login(request: AuthRequest):
    stored_password = get_user(request.email)
    
    if stored_password and stored_password == request.password:
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/signup")
async def signup(request: AuthRequest):
    success = add_user(request.email, request.password)
    
    if success:
        return {"status": "success", "message": "Signup successful"}
    else:
        raise HTTPException(status_code=400, detail="Email already exists")
