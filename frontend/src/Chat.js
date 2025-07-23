import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

const SUGGESTED_PROMPTS = [
  'Should I keep studying or take a break?',
  'How can I manage my time better this week?',
  'What is a good way to relax right now?',
  'How do I balance school and personal time?',
  'Give me a calming strategy.'
];

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || (window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api');

export default function Chat({ onSend, selectedChat }) {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSuggestedPrompts, setShowSuggestedPrompts] = useState(true);
  const messagesEndRef = useRef(null);

  // Use messages from selectedChat or default welcome message
  const messages = selectedChat && selectedChat.messages && selectedChat.messages.length > 0
    ? selectedChat.messages
    : [
        { sender: 'assistant', text: 'Hi! How can I help you with your study-life balance today?' }
      ];

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Show/hide suggested prompts based on whether it's a new chat
  useEffect(() => {
    if (selectedChat && selectedChat.messages && selectedChat.messages.length > 1) {
      setShowSuggestedPrompts(false);
    } else {
      setShowSuggestedPrompts(true);
    }
  }, [selectedChat]);

  const handleSend = async (text) => {
    if (!text.trim() || loading) return;
    setShowSuggestedPrompts(false);
    setInput('');
    setLoading(true);
    // Add user message and 'Typing...' message
    if (onSend) {
      await onSend(text);
    }
    setLoading(false);
  };

  return (
    <div className="chat-box">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`msg ${msg.sender}`}>{msg.text}</div>
        ))}
        {loading && <div className="msg assistant">Thinking...</div>}
        <div ref={messagesEndRef} /> {/* Invisible element for auto-scroll */}
      </div>
      {showSuggestedPrompts && (
        <div className="suggested-prompts">
          {SUGGESTED_PROMPTS.map((prompt, i) => (
            <button key={i} onClick={() => handleSend(prompt)} disabled={loading}>{prompt}</button>
          ))}
        </div>
      )}
      <div className="input-row">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your question..."
          onKeyDown={e => { if (e.key === 'Enter') handleSend(input); }}
          disabled={loading}
        />
        <button onClick={() => handleSend(input)} disabled={loading}>Send</button>
      </div>
    </div>
  );
} 