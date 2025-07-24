import React, { useState } from 'react';
import './AuthModal.css';

export default function AuthModal({ isOpen, onClose, onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const endpoint = isRegister ? '/api/register' : '/api/login';
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();
      if (response.ok && data.access_token) {
        onLogin(data.access_token, email);
      } else {
        setError(data.detail || 'Authentication failed');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-modal-overlay">
      <div className="auth-modal">
        <button className="close-btn" onClick={onClose}>×</button>
        <h2>{isRegister ? 'Register' : 'Login'}</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
          {error && <div className="auth-error">{error}</div>}
          <button type="submit" disabled={loading} className="auth-submit-btn">
            {loading ? 'Please wait...' : (isRegister ? 'Register' : 'Login')}
          </button>
        </form>
        <div className="auth-toggle">
          {isRegister ? (
            <span>Already have an account? <button onClick={() => setIsRegister(false)}>Login</button></span>
          ) : (
            <span>Don&apos;t have an account? <button onClick={() => setIsRegister(true)}>Register</button></span>
          )}
        </div>
      </div>
    </div>
  );
} 