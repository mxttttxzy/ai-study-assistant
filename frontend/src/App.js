import React, { useState, useEffect } from 'react';
import './App.css';
import Chat from './Chat';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);

  // Load chat history from localStorage on mount
  useEffect(() => {
    const anonymousChats = JSON.parse(localStorage.getItem('anonymousChats') || '[]');
    setChatHistory(anonymousChats);
  }, []);

  const handleSendMessage = async (message) => {
    // Simulate backend call (replace with actual fetch if needed)
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
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
    return data.response;
  };

  const formatChatTitle = (message) => {
    const words = message.split(' ').slice(0, 6);
    let title = words.join(' ');
    if (message.length > 40) {
      title = title + '...';
    }
    if (title.length < 10 && message.length > 10) {
      const moreWords = message.split(' ').slice(0, 8);
      title = moreWords.join(' ');
      if (message.length > 50) {
        title = title + '...';
      }
    }
    return title || 'New conversation';
  };

  return (
    <div className="app-background">
      <div className="main-container">
        <div className="chat-history-sidebar">
          <div className="sidebar-header">
            <h3>Chat History</h3>
            <button className="new-chat-btn" onClick={() => setSelectedChat(null)}>+ New Chat</button>
          </div>
          <div className="chat-history-list">
            {chatHistory.length === 0 ? (
              <div className="no-chats">No chats yet.</div>
            ) : (
              chatHistory.slice().reverse().map((chat) => (
                <div
                  key={chat.id}
                  className={`chat-history-item${selectedChat && selectedChat.id === chat.id ? ' selected' : ''}`}
                  onClick={() => setSelectedChat(chat)}
                >
                  <div className="chat-title">{formatChatTitle(chat.message)}</div>
                  <div className="chat-date">{new Date(chat.timestamp).toLocaleString()}</div>
                </div>
              ))
            )}
          </div>
        </div>
        <div className="chat-container">
          <Chat onSend={handleSendMessage} selectedChat={selectedChat} />
        </div>
      </div>
    </div>
  );
}

export default App; 