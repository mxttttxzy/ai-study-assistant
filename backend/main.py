from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import httpx
import os
from typing import List, Optional
import jwt

from database import get_db
from models import User, Chat, Reminder
from auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    ALGORITHM
)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    last_assistant: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ReminderCreate(BaseModel):
    title: str
    description: str
    due_date: datetime

class ReminderResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Free AI Service Configuration
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN", "")  # Optional for some models

# Helper function to get current user (required for protected endpoints)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Helper function to get current user (optional for chat)
def get_current_user_optional(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except jwt.PyJWTError:
        return None
    
    user = get_user_by_email(db, email=email)
    return user

def generate_ai_response(user_message: str, last_assistant: Optional[str] = None) -> str:
    """Generate a calm, friendly, and general AI response for life balance and well-being, with simple context awareness."""
    try:
        user_message_lower = user_message.lower()
        last_assistant_lower = (last_assistant or '').lower()

        # If last assistant message was a question and user gives a vague answer, follow up
        vague_replies = [
            "nothing much", "not really", "idk", "i don't know", "just school", "not sure", "nah", "nope", "nothing", "just life"
        ]
        if last_assistant and '?' in last_assistant_lower:
            if any(vague in user_message_lower for vague in vague_replies):
                # Try to extract topic from user's reply
                if "school" in user_message_lower:
                    return "School can be a lot sometimes. Is there something specific about school that's been on your mind lately?"
                if "life" in user_message_lower:
                    return "Life can feel overwhelming at times. Is there a part of life that's been especially challenging or rewarding for you recently?"
                return "That's okay! Sometimes it's hard to put things into words. Is there anything—big or small—that's been on your mind, or would you like to talk about something in particular?"

        # Break and rest related
        if any(keyword in user_message_lower for keyword in ["break", "rest", "tired", "exhausted", "burnout"]):
            responses = [
                "It sounds like you might need a break! Taking short breaks can actually improve your focus and energy. Try the Pomodoro technique: 25 minutes of focused work, then a 5-minute break. Your mind and body will thank you.",
                "Remember, breaks aren't wasted time—they're essential for your well-being. Even a few minutes to stretch, breathe, or step outside can help you recharge and return with a clearer mind.",
                "It's okay to pause and rest. Sometimes the best way to move forward is to give yourself permission to relax for a bit."
            ]
            return responses[len(user_message) % len(responses)]

        # Time management
        elif any(keyword in user_message_lower for keyword in ["time", "schedule", "plan", "organize", "manage"]):
            responses = [
                "Time management is about finding what works for you. Try making a simple list of your top priorities for the day, and give yourself permission to adjust as needed.",
                "A gentle routine can help bring structure to your day. Block out time for work, rest, and things you enjoy. Remember, it's okay if things don't go perfectly—progress is what matters.",
                "Balance comes from being kind to yourself. If your schedule feels overwhelming, see if you can simplify or delegate a task. Small steps add up."
            ]
            return responses[len(user_message) % len(responses)]

        # Stress and anxiety
        elif any(keyword in user_message_lower for keyword in ["stress", "anxiety", "overwhelmed", "pressure", "worried"]):
            responses = [
                "When things feel overwhelming, try to pause and take a few slow, deep breaths. Remind yourself that it's okay to feel this way, and that you can take things one step at a time.",
                "Stress is a normal part of life, but it doesn't define you. Try grounding yourself in the present moment—notice what you can see, hear, and feel right now.",
                "If you're feeling anxious, remember to be gentle with yourself. Sometimes talking to a friend or taking a short walk can help shift your perspective."
            ]
            return responses[len(user_message) % len(responses)]

        # Balance and personal life
        elif any(keyword in user_message_lower for keyword in ["balance", "personal", "life", "social", "friends", "family"]):
            responses = [
                "Finding balance is a journey, not a destination. Make time for things that bring you joy, whether that's connecting with others or enjoying a quiet moment alone.",
                "Your well-being matters. Try to set gentle boundaries between work and personal time, and remember to celebrate the small wins along the way.",
                "It's important to nurture your relationships and your own interests. Even a short call with a friend or a favorite hobby can help you feel more grounded."
            ]
            return responses[len(user_message) % len(responses)]

        # Study techniques
        elif any(keyword in user_message_lower for keyword in ["study", "learn", "exam", "test", "homework", "assignment"]):
            responses = [
                "Effective learning is about quality, not just quantity. Try summarizing what you've learned in your own words, or teaching it to someone else.",
                "Take regular breaks and be kind to yourself if you get stuck. Sometimes stepping away for a moment helps you see things more clearly when you return.",
                "Remember, it's okay to ask for help or try a new approach if something isn't working. Learning is a process, and you're doing your best."
            ]
            return responses[len(user_message) % len(responses)]

        # Sleep and health
        elif any(keyword in user_message_lower for keyword in ["sleep", "tired", "energy", "health", "exercise"]):
            responses = [
                "Good sleep and gentle movement are the foundation of well-being. Try to keep a regular sleep schedule and move your body in ways that feel good to you.",
                "Even a short walk or a few stretches can boost your mood and energy. Listen to your body and give it the care it needs.",
                "Nourishing your body with food, rest, and kindness helps you show up as your best self."
            ]
            return responses[len(user_message) % len(responses)]

        # Motivation and encouragement
        elif any(keyword in user_message_lower for keyword in ["motivation", "give up", "can't", "impossible", "hard"]):
            responses = [
                "It's okay to have ups and downs. Progress isn't always linear, but every small step counts. Be proud of what you've accomplished so far.",
                "When things feel tough, remember why you started and give yourself credit for showing up. You're stronger than you think.",
                "You don't have to do everything perfectly. Being gentle with yourself is a strength, not a weakness."
            ]
            return responses[len(user_message) % len(responses)]

        else:
            generic_responses = [
                "I'm here to listen and support you. What's been on your mind lately?",
                "If there's something you'd like to talk about, I'm here. Is there a topic or feeling you'd like to explore?",
                "Sometimes just chatting can help. Is there anything you'd like advice or encouragement about today?"
            ]
            return generic_responses[len(user_message) % len(generic_responses)]
    except Exception as e:
        return "I'm here to help you find balance and well-being. Try asking me about time management, stress relief, or anything else on your mind!"

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest, current_user: Optional[User] = Depends(get_current_user_optional), db: Session = Depends(get_db)):
    # Generate AI response using our free service
    ai_response = generate_ai_response(req.message, req.last_assistant)
    
    # Save to database if user is logged in
    if current_user:
        chat = Chat(
            user_id=current_user.id,
            message=req.message,
            response=ai_response
        )
        db.add(chat)
        db.commit()
    
    return {"response": ai_response}

@app.get("/chat/history")
def get_chat_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.timestamp.desc()).limit(50).all()
    return chats

@app.post("/reminders")
def create_reminder(reminder: ReminderCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_reminder = Reminder(
        user_id=current_user.id,
        title=reminder.title,
        description=reminder.description,
        due_date=reminder.due_date
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

@app.get("/reminders")
def get_reminders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reminders = db.query(Reminder).filter(Reminder.user_id == current_user.id).order_by(Reminder.due_date).all()
    return reminders

@app.put("/reminders/{reminder_id}/complete")
def complete_reminder(reminder_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == current_user.id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    reminder.completed = True
    db.commit()
    return reminder 