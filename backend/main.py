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
    history: Optional[List[dict]] = None

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

def detect_user_character(history: Optional[List[dict]]) -> dict:
    """Analyze conversation history to infer user character traits (mood, directness, verbosity, emotional state)."""
    if not history or len(history) < 2:
        return {"mood": "neutral", "directness": "neutral", "verbosity": "neutral", "emotion": "neutral"}
    user_msgs = [m['text'] for m in history if m['sender'] == 'user']
    if not user_msgs:
        return {"mood": "neutral", "directness": "neutral", "verbosity": "neutral", "emotion": "neutral"}
    # Simple heuristics for demo purposes
    last_user = user_msgs[-1]
    mood = "positive" if any(w in last_user.lower() for w in ["happy", "good", "great", "excited"]) else (
        "negative" if any(w in last_user.lower() for w in ["sad", "tired", "bad", "upset", "stressed", "fail"]) else "neutral"
    )
    directness = "direct" if len(last_user.split()) < 8 else "verbose"
    verbosity = "verbose" if len(last_user) > 80 else "concise"
    emotion = "emotional" if any(w in last_user.lower() for w in ["love", "hate", "angry", "scared", "worried"]) else "neutral"
    return {"mood": mood, "directness": directness, "verbosity": verbosity, "emotion": emotion}


def select_conversation_module(user_message: str, user_character: dict) -> str:
    """Select a conversation module based on user message and character."""
    msg = user_message.lower()
    if any(w in msg for w in ["study", "exam", "test", "homework", "assignment"]):
        return "study_support"
    if any(w in msg for w in ["stress", "anxiety", "overwhelmed", "pressure", "worried"]):
        return "emotional_support"
    if any(w in msg for w in ["motivation", "give up", "can't", "impossible", "hard"]):
        return "motivation"
    if any(w in msg for w in ["break", "rest", "tired", "burnout"]):
        return "wellbeing"
    if any(w in msg for w in ["plan", "schedule", "organize", "manage", "time"]):
        return "time_management"
    if user_character["mood"] == "negative":
        return "emotional_support"
    return "general"


def generate_ai_response(user_message: str, last_assistant: Optional[str] = None, history: Optional[List[dict]] = None) -> str:
    """Generate a more adaptive, OpenAI-like response with user character and conversation modules, with added humor and empathy."""
    try:
        user_character = detect_user_character(history)
        module = select_conversation_module(user_message, user_character)
        user_message_lower = user_message.lower()
        last_assistant_lower = (last_assistant or '').lower()
        # Humor for negative mood
        def humorous_empathy():
            jokes = [
                "Remember, even Google doesn't have all the answers. But I'm here to help you search for them!",
                "If life feels like a test, just remember: you can always ask for hints (that's what I'm here for).",
                "If you feel like you're failing, just remember—so did the first pancake. And everyone loves pancakes!",
                "If your brain feels like mashed potatoes, that's okay. Sometimes the best ideas come with a side of gravy!"
            ]
            return f"I'm really sorry to hear that. {jokes[len(user_message) % len(jokes)]} Want to talk more about what's been making you feel this way?"
        # Handle statements (not just questions)
        if user_message_lower.endswith(".") or (user_message_lower and not user_message_lower.endswith("?")):
            # Empathetic statement handling
            if module == "emotional_support":
                if user_character["mood"] == "negative":
                    return humorous_empathy()
                return "That sounds tough. How are you coping with it? If you want, I can share some tips or just listen."
            if module == "study_support":
                return "That can be challenging. Would you like some tips, a quick summary, or just to talk about it?"
            if module == "motivation":
                return "It's normal to feel that way sometimes. What helps you get back on track when things are hard? Or want a pep talk?"
            if module == "wellbeing":
                return "Taking care of yourself is important. What do you usually do to recharge? I can suggest some ideas if you want."
            if module == "time_management":
                return "Managing time can be tricky. Do you want help making a plan, a quick strategy, or just to vent?"
            return "Thanks for sharing that. Is there something specific you'd like to talk about or get advice on?"
        # If user asks for more detail or clarification, build on last AI answer or give a brief explanation
        if history and len(history) > 1:
            last_ai = next((m['text'] for m in reversed(history[:-1]) if m['sender'] == 'assistant'), None)
            last_user = next((m['text'] for m in reversed(history[:-1]) if m['sender'] == 'user'), None)
            if any(kw in user_message_lower for kw in ["more detail", "explain", "expand", "clarify", "what do you mean", "can you elaborate", "why", "how so", "what is", "what's", "not sure", "unsure"]):
                # Try to give a brief, clear explanation
                if last_ai:
                    return f"Of course! To explain: {last_ai} If you want a quick summary or a deeper dive, just let me know."
                # If user is unsure, offer a brief description
                if any(kw in user_message_lower for kw in ["not sure", "unsure"]):
                    return "No worries—it's totally normal to feel unsure. If you tell me what you're stuck on, I can give a quick explanation or some options."
            if last_user and any(topic in user_message_lower for topic in last_user.lower().split()):
                return f"You mentioned '{last_user}'. How has that been going for you since we last talked about it?"
        # Vague replies
        vague_replies = [
            "nothing much", "not really", "idk", "i don't know", "just school", "not sure", "nah", "nope", "nothing", "just life"
        ]
        if last_assistant and '?' in last_assistant_lower:
            if any(vague in user_message_lower for vague in vague_replies):
                if "school" in user_message_lower:
                    return "School can be a lot sometimes. Is there something specific about school that's been on your mind lately? Or want a study meme?"
                if "life" in user_message_lower:
                    return "Life can feel overwhelming at times. Is there a part of life that's been especially challenging or rewarding for you recently? Or should I tell you a fun fact to lighten the mood?"
                return "That's okay! Sometimes it's hard to put things into words. Is there anything—big or small—that's been on your mind, or would you like to talk about something in particular?"
        # Module-based responses
        if module == "study_support":
            responses = [
                "Effective learning is about quality, not just quantity. Try summarizing what you've learned in your own words, or teaching it to someone else.",
                "Take regular breaks and be kind to yourself if you get stuck. Sometimes stepping away for a moment helps you see things more clearly when you return.",
                "Remember, it's okay to ask for help or try a new approach if something isn't working. Learning is a process, and you're doing your best.",
                "If you want a quick tip or a fun study hack, just ask!"
            ]
            return responses[len(user_message) % len(responses)]
        if module == "emotional_support":
            responses = [
                "When things feel overwhelming, try to pause and take a few slow, deep breaths. Remind yourself that it's okay to feel this way, and that you can take things one step at a time.",
                "Stress is a normal part of life, but it doesn't define you. Try grounding yourself in the present moment—notice what you can see, hear, and feel right now.",
                "If you're feeling anxious, remember to be gentle with yourself. Sometimes talking to a friend or taking a short walk can help shift your perspective.",
                "If you want a silly joke or a distraction, just say the word!"
            ]
            return responses[len(user_message) % len(responses)]
        if module == "motivation":
            responses = [
                "It's okay to have ups and downs. Progress isn't always linear, but every small step counts. Be proud of what you've accomplished so far.",
                "When things feel tough, remember why you started and give yourself credit for showing up. You're stronger than you think.",
                "You don't have to do everything perfectly. Being gentle with yourself is a strength, not a weakness.",
                "If you want a pep talk or a motivational quote, just ask!"
            ]
            return responses[len(user_message) % len(responses)]
        if module == "wellbeing":
            responses = [
                "It sounds like you might need a break! Taking short breaks can actually improve your focus and energy. Try the Pomodoro technique: 25 minutes of focused work, then a 5-minute break. Your mind and body will thank you.",
                "Remember, breaks aren't wasted time—they're essential for your well-being. Even a few minutes to stretch, breathe, or step outside can help you recharge and return with a clearer mind.",
                "It's okay to pause and rest. Sometimes the best way to move forward is to give yourself permission to relax for a bit.",
                "If you want a quick breathing exercise or a funny distraction, let me know!"
            ]
            return responses[len(user_message) % len(responses)]
        if module == "time_management":
            responses = [
                "Time management is about finding what works for you. Try making a simple list of your top priorities for the day, and give yourself permission to adjust as needed.",
                "A gentle routine can help bring structure to your day. Block out time for work, rest, and things you enjoy. Remember, it's okay if things don't go perfectly—progress is what matters.",
                "Balance comes from being kind to yourself. If your schedule feels overwhelming, see if you can simplify or delegate a task. Small steps add up.",
                "If you want a quick time-saving tip or a fun productivity fact, just ask!"
            ]
            return responses[len(user_message) % len(responses)]
        # General fallback
        generic_responses = [
            "I'm here to listen and support you. What's been on your mind lately?",
            "If there's something you'd like to talk about, I'm here. Is there a topic or feeling you'd like to explore?",
            "Sometimes just chatting can help. Is there anything you'd like advice or encouragement about today?",
            "If you want a joke, a tip, or just to vent, I'm all ears!"
        ]
        # Adjust tone based on user character
        if user_character["directness"] == "direct":
            return "Let me know what you need, and I'll get right to it. Or if you want a quick laugh, just say so!"
        if user_character["mood"] == "positive":
            return "Love the positive energy! What's been going well for you? Want to celebrate with a fun fact?"
        if user_character["emotion"] == "emotional":
            return "I can tell this means a lot to you. Want to share more, or should I try to lighten the mood?"
        return generic_responses[len(user_message) % len(generic_responses)]
    except Exception as e:
        return "I'm here to help you find balance and well-being. Try asking me about time management, stress relief, or anything else on your mind! If you want a joke, just ask!"

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
    ai_response = generate_ai_response(req.message, req.last_assistant if hasattr(req, 'last_assistant') else None, req.history)
    
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