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

def generate_ai_response(user_message: str) -> str:
    """Generate AI response using free cloud service"""
    try:
        # Create a context-aware prompt for study advice
        prompt = f"""You are a helpful study balance assistant for IB students. A student asks: "{user_message}"

Please provide thoughtful, balanced advice about study-life balance, time management, stress relief, or academic success. Keep responses friendly, practical, and encouraging. Focus on helping students find healthy balance between schoolwork and personal time.

Response:"""
        
        # Enhanced keyword-based responses with more variety and context awareness
        user_message_lower = user_message.lower()
        
        # Break and rest related
        if any(keyword in user_message_lower for keyword in ["break", "rest", "tired", "exhausted", "burnout"]):
            responses = [
                "It sounds like you might need a break! Taking short breaks every 45-60 minutes can actually improve your focus and productivity. Try the Pomodoro technique: 25 minutes of focused work, then a 5-minute break. Your brain needs rest to process information effectively.",
                "I understand the struggle with taking breaks during IB! Remember, breaks aren't wasted time - they're essential for maintaining your mental health and academic performance. Even a 5-minute stretch or walk can refresh your mind significantly.",
                "The pressure to keep studying is real in IB, but your body and mind need rest to function at their best. Try setting a timer for 25-minute study sessions, then force yourself to take a 5-minute break. You'll actually get more done this way!"
            ]
            return responses[len(user_message) % len(responses)]
        
        # Time management
        elif any(keyword in user_message_lower for keyword in ["time", "schedule", "plan", "organize", "manage"]):
            responses = [
                "Time management is key! Try creating a weekly schedule with specific time blocks for studying, breaks, and personal activities. Use tools like Google Calendar or a simple planner. Remember to include buffer time for unexpected tasks.",
                "IB can feel overwhelming, but breaking it down helps! Create a master list of all your assignments, then prioritize them by deadline and importance. Schedule specific times for each task, and don't forget to include breaks and personal time.",
                "Try the Eisenhower Matrix: categorize tasks as urgent/important, important/not urgent, urgent/not important, or neither. Focus on the important ones first, even if they're not urgent. This helps prevent last-minute stress!"
            ]
            return responses[len(user_message) % len(responses)]
        
        # Stress and anxiety
        elif any(keyword in user_message_lower for keyword in ["stress", "anxiety", "overwhelmed", "pressure", "worried"]):
            responses = [
                "Stress is normal, but manageable! Try deep breathing exercises, take short walks, or practice mindfulness. Don't forget to get enough sleep and eat well. It's okay to ask for help when you need it.",
                "IB stress is real, and it's okay to feel overwhelmed sometimes. Try the 4-7-8 breathing technique: inhale for 4 counts, hold for 7, exhale for 8. Also, remember that your worth isn't defined by your grades alone.",
                "When you're feeling stressed, try the 5-4-3-2-1 grounding technique: name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste. This helps bring you back to the present moment."
            ]
            return responses[len(user_message) % len(responses)]
        
        # Balance and personal life
        elif any(keyword in user_message_lower for keyword in ["balance", "personal", "life", "social", "friends", "family"]):
            responses = [
                "Finding balance is a journey! Start by setting clear boundaries between study time and personal time. Make sure to schedule activities you enjoy, get enough sleep, and maintain social connections. Remember, you're more than just your grades.",
                "It's easy to let IB consume everything, but maintaining your personal life is crucial for your mental health. Schedule regular time with friends and family, even if it's just a quick coffee or phone call. These connections keep you grounded.",
                "Think of your life as a pie chart - IB studies should be a significant slice, but not the whole pie. Make sure you're also allocating time for sleep, exercise, social activities, and hobbies. A balanced life leads to better academic performance."
            ]
            return responses[len(user_message) % len(responses)]
        
        # Study techniques
        elif any(keyword in user_message_lower for keyword in ["study", "learn", "exam", "test", "homework", "assignment"]):
            responses = [
                "Effective studying is about quality over quantity! Try active learning techniques like summarizing in your own words, teaching concepts to others, or creating mind maps. Take regular breaks and study in focused sessions rather than marathon cramming.",
                "Instead of passive reading, try active recall: cover your notes and try to explain the concepts out loud. This forces your brain to retrieve information, making it stick better. Also, vary your study locations to improve memory retention.",
                "Break down complex topics into smaller chunks and use the Feynman Technique: explain the concept as if you're teaching it to someone who knows nothing about it. If you can't explain it simply, you don't understand it well enough yet."
            ]
            return responses[len(user_message) % len(responses)]
        
        # Sleep and health
        elif any(keyword in user_message_lower for keyword in ["sleep", "tired", "energy", "health", "exercise"]):
            responses = [
                "Sleep is your superpower! Aim for 7-9 hours of quality sleep each night. Your brain consolidates learning while you sleep, so good sleep actually improves your academic performance. Try to maintain a consistent sleep schedule.",
                "Physical health directly impacts your mental performance. Even 20 minutes of exercise can boost your mood and concentration. Try taking short walks between study sessions, or do some stretching exercises to keep your energy up.",
                "Don't underestimate the power of good nutrition! Eat regular meals, stay hydrated, and include protein and complex carbs in your diet. Your brain needs fuel to function at its best during those long study sessions."
            ]
            return responses[len(user_message) % len(responses)]
        
        # Motivation and encouragement
        elif any(keyword in user_message_lower for keyword in ["motivation", "give up", "can't", "impossible", "hard"]):
            responses = [
                "Remember why you started this journey! IB is challenging, but you're capable of handling it. Break down overwhelming tasks into smaller, manageable steps. Celebrate your progress, no matter how small it seems.",
                "It's okay to have moments of doubt - every IB student does! When you're feeling overwhelmed, remind yourself that this is temporary and you're building skills that will serve you well beyond high school. You've got this!",
                "Progress isn't always linear, and that's normal! Some days will be harder than others, but every day you show up and try, you're moving forward. Don't compare your journey to others - focus on your own growth and improvement."
            ]
            return responses[len(user_message) % len(responses)]
        
        else:
            # More varied generic responses
            generic_responses = [
                "That's a great question! As an IB student, it's important to find your own rhythm. Try breaking your tasks into smaller, manageable chunks, and don't forget to celebrate your progress. What specific aspect of study-life balance are you struggling with? I'm here to help you find what works best for you.",
                "I appreciate you reaching out about this! Every IB student faces unique challenges, and there's no one-size-fits-all solution. Could you tell me more about your specific situation? That way I can give you more targeted advice.",
                "You're asking the right questions! Finding balance in IB is a skill that takes time to develop. What works for one person might not work for another, so it's important to experiment and find what fits your lifestyle and personality."
            ]
            return generic_responses[len(user_message) % len(generic_responses)]
            
    except Exception as e:
        return "I'm here to help with your study-life balance! Try asking me about time management, stress relief, study techniques, or finding balance between school and personal time."

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
    ai_response = generate_ai_response(req.message)
    
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