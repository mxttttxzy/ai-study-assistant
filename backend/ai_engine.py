import os
import json
import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import httpx
import hashlib
import random

class AIEngine:
    def __init__(self):
        self.memory = []
        
        # Available free models
        self.free_models = {
            "huggingface-free": {
                "name": "HuggingFace Free",
                "url": "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                "max_tokens": 2048,
                "cost": "FREE"
            },
            "ollama-local": {
                "name": "Ollama Local",
                "url": "http://localhost:11434/api/generate",
                "max_tokens": 4096,
                "cost": "FREE"
            },
            "community-free": {
                "name": "Community Models",
                "url": "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                "max_tokens": 2048,
                "cost": "FREE"
            },
            "fallback-enhanced": {
                "name": "Enhanced Local (Offline)",
                "url": "local",
                "max_tokens": 2048,
                "cost": "FREE"
            }
        }
        
        # Default model - prioritize offline option
        self.default_model = "fallback-enhanced"
        
    def get_available_models(self) -> List[str]:
        """Get list of available free models"""
        available = ["fallback-enhanced"]  # Always available
        
        # Add external models if token is available
        token = os.environ.get('HUGGINGFACE_TOKEN', '')
        if token:
            available.extend(["huggingface-free", "community-free"])
        
        # Check if Ollama is running locally
        if self._check_ollama_available():
            available.append("ollama-local")
        
        return available
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            response = httpx.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    async def generate_response(
        self, 
        message: str, 
        history: List[Dict] = None,
        model: str = None,
        user_context: Dict = None,
        documents: List[str] = None
    ) -> Dict[str, Any]:
        """Generate AI response using free services"""
        
        model = model or self.default_model
        available_models = self.get_available_models()
        
        # If requested model is not available, fall back to default
        if model not in available_models:
            print(f"Model {model} not available, falling back to {self.default_model}")
            model = self.default_model
        
        # Build context
        context = self._build_context(message, history, user_context, documents)
        
        # Generate response based on free model
        if model == "ollama-local":
            response = await self._generate_ollama_response(context)
        elif model == "huggingface-free":
            response = await self._generate_huggingface_response(context)
        elif model == "community-free":
            response = await self._generate_community_response(context)
        elif model == "fallback-enhanced":
            response = await self._generate_fallback_response(context)
        else:
            # Final fallback
            response = await self._generate_fallback_response(context)
        
        # Update memory
        self.memory.append({
            "input": message,
            "output": response["content"],
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 interactions
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]
        
        return response
    
    def _build_context(
        self, 
        message: str, 
        history: List[Dict] = None,
        user_context: Dict = None,
        documents: List[str] = None
    ) -> str:
        """Build comprehensive context for the AI"""
        
        context_parts = []
        
        # System prompt
        system_prompt = self._get_system_prompt(user_context)
        context_parts.append(f"System: {system_prompt}")
        
        # User context
        if user_context:
            context_parts.append(f"User Profile: {json.dumps(user_context)}")
        
        # Document context
        if documents:
            doc_context = self._process_documents(documents, message)
            if doc_context:
                context_parts.append(f"Relevant Documents: {doc_context}")
        
        # Conversation history
        if history:
            history_text = self._format_history(history)
            context_parts.append(f"Conversation History: {history_text}")
        
        # Current message
        context_parts.append(f"Current Message: {message}")
        
        return "\n\n".join(context_parts)
    
    def _get_system_prompt(self, user_context: Dict = None) -> str:
        """Generate personalized system prompt for students"""
        
        base_prompt = """You are an intelligent, empathetic AI study assistant designed to help students maintain a healthy balance between academics and personal well-being. You provide thoughtful, evidence-based advice while being supportive and encouraging.

Key capabilities:
- Study strategies and time management
- Stress management and mental health support
- Academic planning and goal setting
- Work-life balance guidance
- Code review and programming help
- Document analysis and summarization

Always be:
- Empathetic and understanding
- Evidence-based in your advice
- Encouraging and supportive
- Clear and actionable
- Respectful of individual differences
- Focused on student well-being and success"""
        
        if user_context:
            style = user_context.get("communication_style", "neutral")
            level = user_context.get("study_level", "high_school")
            
            if style == "formal":
                base_prompt += "\n\nUse formal, academic language appropriate for professional communication."
            elif style == "casual":
                base_prompt += "\n\nUse friendly, conversational language with appropriate humor and warmth."
            
            if level == "university":
                base_prompt += "\n\nProvide advanced academic guidance suitable for university-level students."
            elif level == "high_school":
                base_prompt += "\n\nProvide guidance appropriate for high school students, considering their developmental stage."
        
        return base_prompt
    
    def _process_documents(self, documents: List[str], query: str) -> str:
        """Process and retrieve relevant document content"""
        if not documents:
            return ""
        
        # Simple keyword matching for now
        relevant_content = []
        for doc in documents:
            if any(keyword in doc.lower() for keyword in query.lower().split()):
                relevant_content.append(doc[:500] + "..." if len(doc) > 500 else doc)
        
        return "\n".join(relevant_content)
    
    def _format_history(self, history: List[Dict]) -> str:
        """Format conversation history"""
        if not history:
            return ""
        
        formatted = []
        for msg in history[-5:]:  # Last 5 messages
            role = msg.get("sender", "user")
            content = msg.get("text", "")
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    async def _generate_ollama_response(self, context: str) -> Dict[str, Any]:
        """Generate response using Ollama local API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": "mistral",  # Free model
                        "prompt": context,
                        "stream": False
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "content": data.get("response", ""),
                        "model": "ollama-mistral",
                        "tokens_used": len(context.split()),
                        "provider": "ollama-local"
                    }
                else:
                    print(f"Ollama API error: {response.status_code}")
                    return await self._generate_fallback_response(context)
                    
        except Exception as e:
            print(f"Ollama error: {e}")
            return await self._generate_fallback_response(context)
    
    async def _generate_huggingface_response(self, context: str) -> Dict[str, Any]:
        """Generate response using HuggingFace free API"""
        try:
            # Check if we have a token
            token = os.environ.get('HUGGINGFACE_TOKEN', '')
            if not token:
                print("No HuggingFace token provided, falling back to local model")
                return await self._generate_fallback_response(context)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    json={"inputs": context},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    # Extract response from HuggingFace format
                    if isinstance(data, list) and len(data) > 0:
                        content = data[0].get("generated_text", "")
                        # Clean up the response
                        if context in content:
                            content = content.replace(context, "").strip()
                    else:
                        content = str(data)
                    
                    return {
                        "content": content,
                        "model": "huggingface-dialoGPT",
                        "tokens_used": len(context.split()),
                        "provider": "huggingface-free"
                    }
                else:
                    print(f"HuggingFace API error: {response.status_code}")
                    return await self._generate_fallback_response(context)
                    
        except Exception as e:
            print(f"HuggingFace error: {e}")
            return await self._generate_fallback_response(context)
    
    async def _generate_community_response(self, context: str) -> Dict[str, Any]:
        """Generate response using community models"""
        try:
            # Check if we have a token
            token = os.environ.get('HUGGINGFACE_TOKEN', '')
            if not token:
                print("No HuggingFace token provided, falling back to local model")
                return await self._generate_fallback_response(context)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    json={"inputs": context},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = str(data) if isinstance(data, str) else str(data)
                    
                    return {
                        "content": content,
                        "model": "community-blenderbot",
                        "tokens_used": len(context.split()),
                        "provider": "community-free"
                    }
                else:
                    print(f"Community API error: {response.status_code}")
                    return await self._generate_fallback_response(context)
                    
        except Exception as e:
            print(f"Community model error: {e}")
            return await self._generate_fallback_response(context)
    
    async def _generate_fallback_response(self, context: str) -> Dict[str, Any]:
        """Generate intelligent fallback response using local logic"""
        # Enhanced fallback with better context understanding
        context_lower = context.lower()
        
        # Study-related queries
        if any(word in context_lower for word in ["study", "homework", "assignment", "exam", "test"]):
            content = """I understand you're working on your studies! Here are some proven strategies:

📚 **Study Techniques:**
• Break your work into 25-minute focused sessions (Pomodoro Technique)
• Create mind maps or visual summaries
• Teach the material to someone else (or even a pet!)
• Use active recall instead of passive reading

💡 **Pro Tips:**
• Study your hardest subjects when your mind is freshest
• Create a comfortable, distraction-free study space
• Take regular breaks to maintain focus
• Get enough sleep - it's crucial for memory consolidation

Would you like me to elaborate on any of these techniques or help you create a study plan?"""
        
        # Stress and mental health
        elif any(word in context_lower for word in ["stress", "anxiety", "overwhelmed", "tired", "burnout"]):
            content = """It's completely normal to feel stressed about your studies. Your feelings are valid! Here are some calming strategies:

🧘 **Immediate Relief:**
• Take 5 deep breaths: inhale for 4, hold for 4, exhale for 4
• Step away for a 10-minute walk outside
• Listen to calming music or nature sounds
• Text a friend or family member

💪 **Long-term Wellness:**
• Establish a consistent sleep schedule
• Practice regular exercise (even just walking)
• Keep a gratitude journal
• Remember: your worth isn't defined by grades

How are you feeling right now? I'm here to listen and support you."""
        
        # Time management
        elif any(word in context_lower for word in ["time", "schedule", "busy", "overwhelmed", "plan"]):
            content = """Time management is a skill that takes practice! Here's a simple approach:

⏰ **Daily Planning:**
• List your top 3 priorities for the day
• Use time blocking (dedicate specific times to tasks)
• Include buffer time for unexpected events
• Schedule breaks and fun activities too!

📅 **Weekly Strategy:**
• Plan your week on Sunday evening
• Batch similar tasks together
• Don't overcommit - it's okay to say no
• Leave room for flexibility

🎯 **Pro Tips:**
• Use the 2-minute rule: if it takes less than 2 minutes, do it now
• Eliminate distractions (phone in another room)
• Reward yourself after completing tasks
• Be kind to yourself when things don't go perfectly

Would you like help creating a specific schedule or time management plan?"""
        
        # Break and rest
        elif any(word in context_lower for word in ["break", "rest", "tired", "exhausted"]):
            content = """Taking breaks is essential for your well-being and productivity! Here are some great break ideas:

☕ **Short Breaks (5-10 minutes):**
• Stretch or do some light exercises
• Get a glass of water and step outside
• Listen to your favorite song
• Do some deep breathing exercises

🎮 **Medium Breaks (15-30 minutes):**
• Take a walk around your neighborhood
• Call a friend or family member
• Read something for pleasure
• Do a quick hobby activity

🌟 **Longer Breaks:**
• Watch an episode of your favorite show
• Take a nap (20-30 minutes max)
• Do something creative (draw, write, cook)
• Exercise or play a sport

Remember: breaks aren't wasted time - they're essential for maintaining focus and preventing burnout!"""
        
        # General greeting or casual conversation
        elif any(word in context_lower for word in ["hi", "hello", "hey", "how are you"]):
            content = """Hi there! 👋 I'm your AI study assistant, and I'm here to help you with:

📚 **Academic Support:**
• Study strategies and time management
• Stress relief and mental health
• Academic planning and goal setting
• Work-life balance guidance

💬 **How I can help:**
• Answer questions about your studies
• Provide personalized advice
• Help you create study plans
• Support your mental well-being
• Analyze documents you upload

What would you like to work on today? I'm here to support your academic journey!"""
        
        # Default response
        else:
            content = """I'm here to help you with your studies and well-being! You can ask me about:

📖 **Study Help:**
• Effective study techniques
• Time management strategies
• Academic planning
• Test preparation tips

🧠 **Mental Health:**
• Stress management
• Anxiety relief techniques
• Work-life balance
• Self-care strategies

🎯 **Personal Development:**
• Goal setting and motivation
• Productivity tips
• Building healthy habits
• Finding your learning style

What's on your mind? I'm here to listen and provide helpful guidance!"""
        
        return {
            "content": content,
            "model": "fallback-enhanced",
            "tokens_used": len(content.split()),
            "provider": "local-free"
        }
    
    def create_embedding(self, text: str) -> List[float]:
        """Create simple embedding for text"""
        try:
            # Simple hash-based embedding
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            # Convert hex to list of floats
            embedding = []
            for i in range(0, len(hash_hex), 2):
                if len(embedding) < 384:  # Standard embedding size
                    embedding.append(float(int(hash_hex[i:i+2], 16)) / 255.0)
            # Pad or truncate to 384 dimensions
            while len(embedding) < 384:
                embedding.append(0.0)
            return embedding[:384]
        except Exception as e:
            print(f"Embedding error: {e}")
            return [0.0] * 384
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        try:
            # Simple word overlap similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            return len(intersection) / len(union) if union else 0.0
        except Exception as e:
            print(f"Similarity calculation error: {e}")
            return 0.0

# Global AI engine instance
ai_engine = AIEngine() 