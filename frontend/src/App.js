import React, { useState, useEffect } from 'react';
import './App.css';
import Chat from './Chat';

function App() {
  const [chatHistory, setChatHistory] = useState([]); // Array of {id, messages: [{sender, text, timestamp}], timestamp}
  const [selectedChat, setSelectedChat] = useState(null); // The chat object
  const [chatKey, setChatKey] = useState(0);
  const [currentChat, setCurrentChat] = useState({
    id: Date.now(),
    messages: [
      { sender: 'assistant', text: 'Hi! How can I help you with your study-life balance today?', timestamp: new Date().toISOString() }
    ],
    timestamp: new Date().toISOString()
  });

  // Load chat history from localStorage on mount
  useEffect(() => {
    const chats = JSON.parse(localStorage.getItem('anonymousChats') || '[]');
    setChatHistory(chats);
  }, []);

  // Save chat history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('anonymousChats', JSON.stringify(chatHistory));
  }, [chatHistory]);

  // When a chat is selected from the sidebar
  useEffect(() => {
    if (selectedChat) {
      setCurrentChat(selectedChat);
    }
  }, [selectedChat]);

  const handleSendMessage = async (message) => {
    // Add user message
    const userMsg = { sender: 'user', text: message, timestamp: new Date().toISOString() };
    let assistantMsg;
    setCurrentChat(prev => ({
      ...prev,
      messages: [...prev.messages, userMsg]
    }));
    // Simulate backend call
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await response.json();
    assistantMsg = { sender: 'assistant', text: data.response, timestamp: new Date().toISOString() };
    setCurrentChat(prev => ({
      ...prev,
      messages: [...prev.messages, assistantMsg]
    }));
    return data.response;
  };

  const handleNewChat = () => {
    // Save current chat to history if it has more than the initial message
    if (currentChat.messages.length > 1) {
      setChatHistory(prev => [...prev, { ...currentChat, timestamp: new Date().toISOString() }]);
    }
    // Start a new chat
    const newChat = {
      id: Date.now(),
      messages: [
        { sender: 'assistant', text: 'Hi! How can I help you with your study-life balance today?', timestamp: new Date().toISOString() }
      ],
      timestamp: new Date().toISOString()
    };
    setCurrentChat(newChat);
    setSelectedChat(null);
    setChatKey(prev => prev + 1);
  };

  const formatChatTitle = (chat) => {
    if (!chat || !chat.messages || chat.messages.length === 0) return 'New conversation';
    const message = chat.messages.find(m => m.sender === 'user')?.text || chat.messages[0].text;
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
            <button className="new-chat-btn" onClick={handleNewChat}>+ New Chat</button>
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
                  style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
                >
                  <div style={{ flex: 1 }}>
                    <div className="chat-title">{formatChatTitle(chat)}</div>
                    <div className="chat-date">{new Date(chat.timestamp).toLocaleString()}</div>
                  </div>
                  <button
                    className="delete-chat-btn"
                    onClick={e => {
                      e.stopPropagation();
                      setChatHistory(prev => prev.filter(c => c.id !== chat.id));
                      if (selectedChat && selectedChat.id === chat.id) {
                        setSelectedChat(null);
                        setCurrentChat({
                          id: Date.now(),
                          messages: [
                            { sender: 'assistant', text: 'Hi! How can I help you with your study-life balance today?', timestamp: new Date().toISOString() }
                          ],
                          timestamp: new Date().toISOString()
                        });
                        setChatKey(prev => prev + 1);
                      }
                    }}
                    style={{ marginLeft: 8, background: 'transparent', border: 'none', color: '#e53e3e', cursor: 'pointer', fontSize: '1.2em' }}
                    title="Delete chat"
                  >
                    ×
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
        <div className="chat-container">
          <Chat key={chatKey} onSend={handleSendMessage} selectedChat={currentChat} />
        </div>
      </div>
    </div>
  );
}

export default App; 