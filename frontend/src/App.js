import React, { useState, useEffect } from 'react';
import './App.css';
import Chat from './Chat';
import Auth from './Auth';
import Reminders from './Reminders';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || (window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api');

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [userEmail, setUserEmail] = useState(localStorage.getItem('userEmail'));
  const [showReminders, setShowReminders] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);

  // Load chat history on component mount
  useEffect(() => {
    if (token) {
      loadChatHistory();
    } else {
      // Load anonymous chat history
      const anonymousChats = JSON.parse(localStorage.getItem('anonymousChats') || '[]');
      setChatHistory(anonymousChats);
    }
  }, [token]);

  const loadChatHistory = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/chat/history`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const history = await response.json();
        setChatHistory(history);
      }
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const handleLogin = (newToken) => {
    setToken(newToken);
    setUserEmail(localStorage.getItem('userEmail'));
  };

  const handleLogout = () => {
    setToken(null);
    setUserEmail(null);
    setChatHistory([]);
    setSelectedChat(null);
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
  };

  const handleSendMessage = async (message) => {
    // Always try the backend first (works for both authenticated and anonymous users)
    try {
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add authorization header if user is logged in
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ message })
      });
      
      if (response.ok) {
        const data = await response.json();
        // Update chat history
        if (token) {
          loadChatHistory(); // Reload from backend
        } else {
          // Update local anonymous chat history
          const anonymousChats = JSON.parse(localStorage.getItem('anonymousChats') || '[]');
          const newChat = {
            id: Date.now(),
            message,
            response: data.response,
            timestamp: new Date().toISOString()
          };
          anonymousChats.push(newChat);
          localStorage.setItem('anonymousChats', JSON.stringify(anonymousChats));
          setChatHistory(anonymousChats);
        }
        return data.response;
      } else {
        throw new Error('Backend request failed');
      }
    } catch (error) {
      // Fallback for anonymous users or network errors
      if (!token) {
        const anonymousChats = JSON.parse(localStorage.getItem('anonymousChats') || '[]');
        const newChat = {
          id: Date.now(),
          message,
          response: 'This is a placeholder response for anonymous users. Please log in for full AI responses.',
          timestamp: new Date().toISOString()
        };
        anonymousChats.push(newChat);
        localStorage.setItem('anonymousChats', JSON.stringify(anonymousChats));
        setChatHistory(anonymousChats);
        return newChat.response;
      }
      return 'Sorry, there was a problem contacting the AI. Please try again.';
    }
  };

  const formatChatTitle = (message) => {
    // Create a more meaningful title from the message
    const words = message.split(' ').slice(0, 6); // Take first 6 words
    let title = words.join(' ');
    
    // If the message is longer, add ellipsis
    if (message.length > 40) {
      title = title + '...';
    }
    
    // If the title is too short, add more words
    if (title.length < 10 && message.length > 10) {
      const moreWords = message.split(' ').slice(0, 8);
      title = moreWords.join(' ');
      if (message.length > 50) {
        title = title + '...';
      }
    }
    
    return title || 'New conversation';
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (!token) {
    return <Auth onLogin={handleLogin} onSignup={handleLogin} />;
  }

  return (
    <div className="app-background">
      <div className="main-container">
        {/* Chat History Sidebar */}
        <div className="chat-history-sidebar">
          <div className="sidebar-header">
            <h3>Chat History</h3>
            <button 
              className="new-chat-btn"
              onClick={() => setSelectedChat(null)}
            >
              New Chat
            </button>
          </div>
          <div className="chat-history-list">
            {chatHistory.length === 0 ? (
              <div className="no-chats">No previous chats</div>
            ) : (
              chatHistory.map((chat, index) => (
                <div 
                  key={chat.id || index}
                  className={`chat-history-item ${selectedChat === index ? 'selected' : ''}`}
                  onClick={() => setSelectedChat(index)}
                >
                  <div className="chat-title">{formatChatTitle(chat.message)}</div>
                  <div className="chat-date">{formatDate(chat.timestamp)}</div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="chat-container">
          <div className="header">
            <h1>AI Study Balance Assistant</h1>
            <div className="user-info">
              <span>Welcome, {userEmail}</span>
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </div>
          </div>
          
          <Chat onSend={handleSendMessage} selectedChat={selectedChat !== null ? chatHistory[selectedChat] : null} />
          
          <div className="features">
            <button 
              onClick={() => setShowReminders(!showReminders)}
              className="toggle-feature-btn"
            >
              {showReminders ? 'Hide Reminders' : 'Show Reminders'}
            </button>
          </div>
          
          {showReminders && <Reminders token={token} />}
        </div>
      </div>
    </div>
  );
}

export default App; 