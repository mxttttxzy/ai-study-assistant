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
  const [messages, setMessages] = useState([
    { sender: 'assistant', text: 'Hi! How can I help you with your study-life balance today?' }
  ]);
  const [loading, setLoading] = useState(false);
  const [showSuggestedPrompts, setShowSuggestedPrompts] = useState(true);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle selected chat changes
  useEffect(() => {
    if (selectedChat) {
      // Display the selected chat
      setMessages([
        { sender: 'user', text: selectedChat.message },
        { sender: 'assistant', text: selectedChat.response }
      ]);
      setShowSuggestedPrompts(false); // Hide prompts when viewing history
    } else {
      // Reset to welcome message for new chat
      setMessages([
        { sender: 'assistant', text: 'Hi! How can I help you with your study-life balance today?' }
      ]);
      setShowSuggestedPrompts(true); // Show prompts for new chat
    }
  }, [selectedChat]);

  const handleSend = async (text) => {
    if (!text.trim() || loading) return;
    
    // Hide suggested prompts after first message
    setShowSuggestedPrompts(false);
    
    setMessages(msgs => [...msgs, { sender: 'user', text }]);
    setInput('');
    setLoading(true);
    
    // Use the onSend prop if provided, otherwise use the old method
    if (onSend) {
      const reply = await onSend(text);
      setMessages(msgs => [...msgs, { sender: 'assistant', text: reply }]);
    } else {
      try {
        const res = await fetch(`${BACKEND_URL}/chat`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        setMessages(msgs => [...msgs, { sender: 'assistant', text: data.response }]);
      } catch (e) {
        setMessages(msgs => [...msgs, { sender: 'assistant', text: 'Sorry, there was a problem contacting the AI.' }]);
      }
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