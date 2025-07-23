from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    preferences = Column(JSON, default={})  # User preferences and settings
    communication_style = Column(String, default="neutral")  # formal, casual, etc.
    study_level = Column(String, default="high_school")  # high_school, university, etc.
    
    chats = relationship("Chat", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    documents = relationship("Document", back_populates="user")
    conversation_embeddings = relationship("ConversationEmbedding", back_populates="user")

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_used = Column(String, default="default")  # Which AI model was used
    tokens_used = Column(Integer, default=0)  # Token usage for cost tracking
    context_length = Column(Integer, default=0)  # Length of context provided
    
    user = relationship("User", back_populates="chats")
    feedback = relationship("Feedback", back_populates="chat")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=True)
    message = Column(Text)
    rating = Column(Integer)  # 1 for positive, -1 for negative
    timestamp = Column(DateTime, default=datetime.utcnow)
    detailed_feedback = Column(Text, nullable=True)  # Optional detailed feedback
    category = Column(String, nullable=True)  # helpfulness, accuracy, relevance, etc.

    chat = relationship("Chat", back_populates="feedback")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    content = Column(Text)
    file_type = Column(String)  # pdf, txt, docx, etc.
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    embeddings = Column(JSON, nullable=True)  # Document embeddings for semantic search
    
    user = relationship("User", back_populates="documents")

class ConversationEmbedding(Base):
    __tablename__ = "conversation_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    conversation_text = Column(Text)
    embedding = Column(JSON)  # Vector embedding of conversation
    timestamp = Column(DateTime, default=datetime.utcnow)
    relevance_score = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="conversation_embeddings")

class Reminder(Base):
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="reminders") 