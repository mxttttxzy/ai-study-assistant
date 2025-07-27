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
  const [topic, setTopic] = useState(null); // Track the current topic
  const [allowInput, setAllowInput] = useState(false); // Control input visibility
  const [offTopicWarning, setOffTopicWarning] = useState(''); // Show off-topic warning
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(new Set()); // Track which messages have feedback
  const [selectedModel, setSelectedModel] = useState('fallback-enhanced'); // Default to offline AI
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
    setOffTopicWarning('');
    // If this is the first message (from a suggestion), set the topic
    if (!topic) {
      setTopic(text);
    } else {
      // Check if the user is off-topic (not a casual message)
      const casual = /\b(thank(s| you)?|bye|see you|goodbye|your welcome|you're welcome|hi|hello)\b/i;
      if (!text.toLowerCase().includes(topic.toLowerCase()) && !casual.test(text)) {
        setOffTopicWarning(`Let's try to stay on topic: "${topic}". You can ask more about it or say 'thanks' if you're done!`);
      }
    }
    setAllowInput(true); // Always allow input after first send
    if (onSend) {
      await onSend(text, selectedModel);
    }
    setLoading(false);
  };

  const handleFeedback = async (messageIndex, rating) => {
    const message = messages[messageIndex];
    if (message.sender === 'assistant' && !feedbackSubmitted.has(messageIndex)) {
      try {
        await fetch('/api/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: message.text,
            rating: rating
          })
        });
        setFeedbackSubmitted(prev => new Set([...prev, messageIndex]));
      } catch (error) {
        console.error('Failed to submit feedback:', error);
      }
    }
  };

  return (
    <div className="chat-box">
      {/* Model Selection - Always visible */}
      <div className="model-selector">
        <label htmlFor="model-select">AI Model: </label>
        <select
          id="model-select"
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="model-dropdown"
        >
          <option value="fallback-enhanced">💡 Enhanced Local (Offline)</option>
          <option value="huggingface-free">🤗 HuggingFace Free</option>
          <option value="community-free">🌐 Community Models</option>
          <option value="ollama-local">🖥️ Ollama Local (if available)</option>
        </select>
      </div>
      
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`msg ${msg.sender}`}>
            {msg.text}
            {msg.sender === 'assistant' && !feedbackSubmitted.has(i) && (
              <div className="feedback-buttons">
                <button 
                  onClick={() => handleFeedback(i, 1)} 
                  className="feedback-btn positive"
                  title="This was helpful"
                >
                  👍
                </button>
                <button 
                  onClick={() => handleFeedback(i, -1)} 
                  className="feedback-btn negative"
                  title="This was not helpful"
                >
                  👎
                </button>
              </div>
            )}
            {msg.sender === 'assistant' && feedbackSubmitted.has(i) && (
              <div className="feedback-submitted">Thanks for your feedback!</div>
            )}
          </div>
        ))}
        {loading && <div className="msg assistant loading">🤔 Thinking about your question...</div>}
        {offTopicWarning && <div className="msg assistant warning">{offTopicWarning}</div>}
        <div ref={messagesEndRef} /> {/* Invisible element for auto-scroll */}
      </div>
      {showSuggestedPrompts && (
        <div className="suggested-prompts">
          {SUGGESTED_PROMPTS.map((prompt, i) => (
            <button key={i} onClick={() => { handleSend(prompt); setAllowInput(true); }} disabled={loading}>{prompt}</button>
          ))}
        </div>
      )}
      {allowInput && (
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
      )}
    </div>
  );
} 