# 🆓 Free AI Study Assistant Setup Guide

## 🎯 For Students - Completely Free!

This AI study assistant is designed specifically for students and is **100% FREE** to use. No paid API keys required!

---

## 🚀 Quick Start (5 minutes)

### Option 1: Use Right Now (No Setup Required)
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-assistant
   ```

2. **Start the application**
   ```bash
   docker compose up --build
   ```

3. **Open your browser**
   - Go to: http://localhost:3000
   - Start chatting immediately!

**That's it!** The AI will work with enhanced local responses - no setup needed.

---

## 🆓 Free AI Options Available

### 1. **Enhanced Local AI** (Always Works)
- ✅ **No internet required**
- ✅ **No API keys needed**
- ✅ **Instant responses**
- ✅ **Student-focused advice**

**Features:**
- Study strategies and time management
- Stress relief and mental health support
- Academic planning and goal setting
- Work-life balance guidance
- Personalized communication style

### 2. **HuggingFace Free** (Best Quality)
- ✅ **Completely free**
- ✅ **High-quality responses**
- ✅ **Requires internet connection**
- ✅ **Optional HuggingFace token** (free to get)

**Setup:**
1. Go to [HuggingFace](https://huggingface.co/)
2. Create a free account
3. Get your free API token
4. Add to `.env` file: `HUGGINGFACE_TOKEN=your-token`

### 3. **Ollama Local** (Fastest)
- ✅ **Runs on your computer**
- ✅ **No internet required**
- ✅ **Fastest responses**
- ✅ **Completely private**

**Setup:**
1. Install [Ollama](https://ollama.ai/)
2. Run: `ollama pull mistral`
3. Start with: `docker compose --profile local-ai up`

---

## 📚 What the AI Can Help With

### 🧠 **Study Support**
- **Study Techniques**: Pomodoro method, active recall, mind mapping
- **Time Management**: Scheduling, prioritization, productivity tips
- **Test Preparation**: Study plans, review strategies, stress management
- **Academic Planning**: Goal setting, course planning, career guidance

### 🧘 **Mental Health & Wellness**
- **Stress Management**: Breathing exercises, relaxation techniques
- **Anxiety Relief**: Coping strategies, grounding exercises
- **Work-Life Balance**: Setting boundaries, self-care practices
- **Motivation**: Goal setting, habit building, positive reinforcement

### 📖 **Document Analysis**
- **Upload Study Materials**: PDFs, documents, notes
- **Get Summaries**: Key points and insights
- **Ask Questions**: About your uploaded content
- **Create Study Guides**: From your materials

### 💬 **Personalized Experience**
- **Communication Style**: Formal, casual, or neutral
- **Study Level**: High school, university, or graduate
- **Learning Preferences**: Visual, auditory, or kinesthetic
- **Feedback System**: Rate responses to improve AI

---

## 🛠️ Advanced Setup (Optional)

### For Better Performance

#### 1. **HuggingFace Setup** (Recommended)
```bash
# 1. Create free account at https://huggingface.co/
# 2. Get your free API token
# 3. Create .env file:
echo "HUGGINGFACE_TOKEN=your-free-token" > .env
```

#### 2. **Local AI Setup** (Fastest)
```bash
# 1. Install Ollama: https://ollama.ai/
# 2. Download a model:
ollama pull mistral

# 3. Start with local AI:
docker compose --profile local-ai up
```

#### 3. **Development Setup**
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

---

## 🎯 How to Use

### 1. **Start a Conversation**
- Click on suggested prompts or type your own
- Ask about study strategies, stress relief, time management
- Upload documents for analysis

### 2. **Get Personalized Help**
- Set your communication style (formal/casual)
- Choose your study level
- Upload study materials
- Rate responses to improve AI

### 3. **Advanced Features**
- **Document Upload**: Drag and drop files for analysis
- **Model Selection**: Choose different AI models
- **Feedback System**: Rate responses with 👍/👎
- **Conversation History**: All chats are saved locally

---

## 💡 Pro Tips for Students

### **Study Sessions**
- Ask: "Help me create a study plan for [subject]"
- Upload your notes and ask questions
- Get time management advice for busy schedules

### **Stress Relief**
- Ask: "I'm feeling overwhelmed with [situation]"
- Get immediate calming strategies
- Learn long-term stress management techniques

### **Academic Planning**
- Ask: "Help me balance [activity] with my studies"
- Get advice on course selection
- Plan for exams and assignments

### **Mental Health**
- Ask: "I'm feeling anxious about [situation]"
- Get coping strategies and support
- Learn self-care practices

---

## 🔧 Troubleshooting

### **AI Not Responding**
- Check internet connection (for HuggingFace)
- Try "Enhanced Local" model (always works)
- Restart the application

### **Slow Responses**
- Switch to "Enhanced Local" for instant responses
- Use Ollama for fastest local performance
- Check your internet connection

### **Document Upload Issues**
- Ensure files are under 10MB
- Supported formats: PDF, TXT, DOC, DOCX
- Check file permissions

---

## 🆓 Why This is Free

### **For Students**
- **No Cost Barriers**: Every student deserves access to AI help
- **Privacy First**: All data stays on your device
- **Open Source**: Transparent and trustworthy
- **Community Driven**: Built by students, for students

### **Free AI Models**
- **HuggingFace**: Free tier with generous limits
- **Ollama**: Completely free local models
- **Local Fallback**: Always available, no internet needed
- **Community Models**: Free open-source alternatives

---

## 🚀 Ready to Start?

1. **Quick Start**: `docker compose up --build`
2. **Open Browser**: http://localhost:3000
3. **Start Chatting**: Ask for study help, stress relief, or academic advice

**Remember**: This is designed specifically for students and is completely free to use! 🎓✨

---

*Built with ❤️ for students everywhere* 