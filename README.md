# 🆓 Free AI Study Balance Assistant

A **completely free**, minimalist, calming AI-powered assistant designed to help students maintain a healthy balance between schoolwork, rest, and personal time. Built with FastAPI, React, and free AI models.

## 🎯 **100% FREE for Students**

- ✅ **No paid API keys required**
- ✅ **No subscription fees**
- ✅ **No usage limits**
- ✅ **Works offline**
- ✅ **Privacy-first design**

---

## Features

### 🤖 **Free AI Chat Assistant**
- **Study-Life Balance Advice**: Get thoughtful, balanced advice on study habits, time management, and relaxation strategies
- **Multiple Free AI Models**: Choose from HuggingFace Free, Community Models, Ollama Local, or Enhanced Local
- **Suggested Prompts**: Quick-access buttons for common questions like "Should I keep studying or take a break?"
- **Offline Support**: Works without internet connection using enhanced local AI
- **Topic Tracking**: AI helps you stay focused and gently guides you back if you go off-topic
- **Feedback System**: Rate responses to help improve the AI's conversational abilities

### 👤 **User Authentication**
- **Email/Password Registration**: Create an account to save your chat history and reminders
- **Secure Login**: JWT-based authentication with password hashing
- **Anonymous Mode**: Use the app without creating an account (limited features)

### 📝 **Chat History**
- **Persistent Storage**: All conversations are saved locally in SQLite database
- **Offline Access**: Chat history persists even when offline
- **Privacy-First**: All data stored locally on your device

### ⏰ **Reminders System**
- **Task Management**: Create reminders with titles, descriptions, and due dates
- **Visual Organization**: Clean, minimalist interface for managing your tasks
- **Completion Tracking**: Mark reminders as complete with a simple click

### 📚 **Document Intelligence**
- **Upload Study Materials**: PDFs, documents, notes for AI analysis
- **Semantic Search**: AI finds relevant content from your documents
- **Study Guides**: Generate summaries and insights from your materials

### 🎨 **Design**
- **Calming Aesthetic**: Soft, gradient background with minimalist UI
- **Responsive Design**: Works on desktop and mobile devices
- **PWA Ready**: Can be installed as a web app for offline access

## 🆓 **Free AI Models Available**

### 1. **Enhanced Local AI** (Always Works)
- ✅ No internet required
- ✅ No API keys needed
- ✅ Instant responses
- ✅ Student-focused advice

### 2. **HuggingFace Free** (Best Quality)
- ✅ Completely free
- ✅ High-quality responses
- ✅ Requires internet connection
- ✅ Optional free token

### 3. **Ollama Local** (Fastest)
- ✅ Runs on your computer
- ✅ No internet required
- ✅ Fastest responses
- ✅ Completely private

### 4. **Community Models** (Alternative)
- ✅ Free open-source models
- ✅ Multiple options available
- ✅ Community-driven

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with SQLite
- **Alembic**: Database migrations
- **JWT Authentication**: Secure user sessions
- **Free AI Integration**: HuggingFace, Ollama, local models

### Frontend
- **React**: Modern JavaScript framework
- **CSS3**: Custom styling with calming color palette
- **LocalStorage**: Offline data persistence
- **Service Workers**: PWA capabilities

### Infrastructure
- **Docker**: Containerized deployment
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Static file serving

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- Python 3.11+ (for local development)
- Node.js 18+ (for local development)

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-assistant
   ```

2. **Start all services** (No setup required!)
   ```bash
   docker compose up --build -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Health Check: http://localhost:8000/health

**That's it!** The AI will work immediately with enhanced local responses.

### Optional: Enhanced Setup

#### For Better Performance (Free)
```bash
# 1. Get free HuggingFace token (optional)
# Go to https://huggingface.co/ and create free account
# Copy your free API token

# 2. Create .env file
echo "HUGGINGFACE_TOKEN=your-free-token" > .env

# 3. Restart the application
docker compose up --build -d
```

#### For Local AI (Fastest)
```bash
# 1. Install Ollama: https://ollama.ai/
# 2. Download free model
ollama pull mistral

# 3. Start with local AI
docker compose --profile local-ai up --build -d
```

### First Time Setup

1. **Create an account** (optional but recommended)
   - Click "Sign Up" on the login screen
   - Enter your email and password
   - Your data will be stored locally

2. **Start chatting**
   - Click on a suggested prompt to begin
   - Type follow-up questions after the AI responds
   - Rate responses with 👍/👎 to help improve the AI

3. **Upload documents** (for logged-in users)
   - Click the settings gear (⚙️) in the sidebar
   - Upload study materials for AI analysis
   - Ask questions about your documents

## Environment Variables

Create a `.env` file based on `env.example` (all optional):

```bash
# Backend Environment Variables
JWT_SECRET_KEY=your-secret-key-here-change-in-production
DATABASE_URL=sqlite:///./ai_assistant.db

# Free AI Services (Optional - for enhanced features)
HUGGINGFACE_TOKEN=your-huggingface-token-here-optional

# AI Configuration
DEFAULT_AI_MODEL=huggingface-free
MAX_TOKENS=2048
TEMPERATURE=0.7

# Frontend Environment Variables
REACT_APP_BACKEND_URL=http://localhost:8000
```

**Note**: The application works completely free without any environment variables!

## Usage Examples

### Chat Prompts
- "Should I keep studying or take a break?"
- "How can I manage my time better this week?"
- "What is a good way to relax right now?"
- "How do I balance school and personal time?"
- "Give me a calming strategy."

### Conversation Flow
1. Click a suggested prompt
2. AI responds with helpful advice
3. Ask follow-up questions
4. Rate responses with 👍 or 👎
5. Say "thanks" when you're done

### Reminders
- Study session reminders
- Assignment due dates
- Break time notifications
- Personal time scheduling

## Deployment

### Render
The project includes `render.yaml` for easy deployment on Render.com.

### Railway
Use the provided `railway.json` for Railway deployment.

### Docker
```bash
docker build -t ai-assistant .
docker run -p 80:80 ai-assistant
```

## 🆓 Why This is Free

### For Students
- **No Cost Barriers**: Every student deserves access to AI help
- **Privacy First**: All data stays on your device
- **Open Source**: Transparent and trustworthy
- **Community Driven**: Built by students, for students

### Free AI Models
- **HuggingFace**: Free tier with generous limits
- **Ollama**: Completely free local models
- **Local Fallback**: Always available, no internet needed
- **Community Models**: Free open-source alternatives

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

**Built with ❤️ for students everywhere - Completely Free! 🎓✨** 