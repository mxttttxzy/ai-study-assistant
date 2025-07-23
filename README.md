# AI Study Balance Assistant

A minimalist, calming AI-powered assistant designed to help IB students maintain a healthy balance between schoolwork, rest, and personal time. Built with FastAPI, React, and Ollama (Mistral model).

## Features

### 🤖 AI Chat Assistant
- **Study-Life Balance Advice**: Get thoughtful, balanced advice on study habits, time management, and relaxation strategies
- **Suggested Prompts**: Quick-access buttons for common questions like "Should I keep studying or take a break?"
- **Offline Support**: Works without internet connection (basic responses for anonymous users)

### 👤 User Authentication
- **Email/Password Registration**: Create an account to save your chat history and reminders
- **Secure Login**: JWT-based authentication with password hashing
- **Anonymous Mode**: Use the app without creating an account (limited features)

### 📝 Chat History
- **Persistent Storage**: All conversations are saved locally in SQLite database
- **Offline Access**: Chat history persists even when offline
- **Privacy-First**: All data stored locally on your device

### ⏰ Reminders System
- **Task Management**: Create reminders with titles, descriptions, and due dates
- **Visual Organization**: Clean, minimalist interface for managing your tasks
- **Completion Tracking**: Mark reminders as complete with a simple click

### 🎨 Design
- **Calming Aesthetic**: Soft, gradient background with minimalist UI
- **Responsive Design**: Works on desktop and mobile devices
- **PWA Ready**: Can be installed as a web app for offline access

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with SQLite
- **JWT Authentication**: Secure user sessions
- **Ollama Integration**: Local AI model (Mistral)

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
- At least 4GB of available RAM (for Ollama)

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-assistant
   ```

2. **Start all services**
   ```bash
   docker compose up --build -d
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Ollama API: http://localhost:11434

### First Time Setup

1. **Create an account** (optional but recommended)
   - Click "Sign Up" on the login screen
   - Enter your email and password
   - Your data will be stored locally

2. **Start chatting**
   - Use the suggested prompts or type your own questions
   - Get AI-powered advice on study-life balance

3. **Add reminders** (for logged-in users)
   - Click "Show Reminders" to access the reminder system
   - Create tasks with due dates and descriptions

## Usage Examples

### Chat Prompts
- "Should I keep studying or take a break?"
- "How can I manage my time better this week?"
- "What is a good way to relax right now?"
- "How do I balance school and personal time?"
- "Give me a calming strategy."

### Reminders
- Study session reminders
- Break time notifications
- Assignment due dates
- Personal time scheduling

## Offline Features

- **Anonymous Chat**: Basic responses without internet
- **Local Storage**: Chat history and reminders persist offline
- **PWA Support**: Install as a web app for better offline experience

## Development

### Project Structure
```
ai-assistant/
├── backend/           # FastAPI application
│   ├── main.py       # Main application file
│   ├── models.py     # Database models
│   ├── auth.py       # Authentication utilities
│   └── database.py   # Database configuration
├── frontend/         # React application
│   ├── src/
│   │   ├── App.js    # Main application component
│   │   ├── Chat.js   # Chat interface
│   │   ├── Auth.js   # Authentication component
│   │   └── Reminders.js # Reminders management
│   └── public/       # Static assets
└── docker-compose.yml # Service orchestration
```

### Adding Features
1. Backend: Add new endpoints in `backend/main.py`
2. Frontend: Create new components in `frontend/src/`
3. Database: Update models in `backend/models.py`
4. Rebuild: `docker compose up --build -d`

## Troubleshooting

### Common Issues

**Docker containers not starting**
- Ensure Docker Desktop is running
- Check available system resources
- Try `docker compose down && docker compose up --build -d`

**AI responses not working**
- Verify Ollama container is running: `docker compose ps`
- Check Ollama logs: `docker compose logs ollama`
- Ensure Mistral model is loaded: `docker compose exec ollama ollama list`

**Authentication issues**
- Clear browser localStorage
- Check backend logs: `docker compose logs backend`

### Performance Tips

- **RAM Usage**: Ollama requires significant memory. Close other applications if needed
- **First Run**: Initial model download may take several minutes
- **Offline Mode**: Use anonymous mode for faster responses when offline

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

---

**Built with ❤️ for IB students everywhere** 