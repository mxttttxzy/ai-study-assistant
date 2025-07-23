import React, { useState, useEffect } from 'react';
import './Reminders.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || (window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api');

export default function Reminders({ token }) {
  const [reminders, setReminders] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (token) {
      fetchReminders();
    }
  }, [token]);

  const fetchReminders = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/reminders`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setReminders(data);
      }
    } catch (error) {
      console.error('Error fetching reminders:', error);
    }
  };

  const addReminder = async (e) => {
    e.preventDefault();
    if (!title.trim() || !dueDate) return;

    setLoading(true);
    try {
      const response = await fetch(`${BACKEND_URL}/reminders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim(),
          due_date: new Date(dueDate).toISOString()
        })
      });

      if (response.ok) {
        setTitle('');
        setDescription('');
        setDueDate('');
        fetchReminders();
      }
    } catch (error) {
      console.error('Error adding reminder:', error);
    }
    setLoading(false);
  };

  const completeReminder = async (id) => {
    try {
      const response = await fetch(`${BACKEND_URL}/reminders/${id}/complete`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        fetchReminders();
      }
    } catch (error) {
      console.error('Error completing reminder:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="reminders-container">
      <h3>Reminders</h3>
      
      <form onSubmit={addReminder} className="reminder-form">
        <input
          type="text"
          placeholder="Reminder title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <input
          type="datetime-local"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add Reminder'}
        </button>
      </form>

      <div className="reminders-list">
        {reminders.length === 0 ? (
          <p>No reminders yet. Add one above!</p>
        ) : (
          reminders.map(reminder => (
            <div key={reminder.id} className={`reminder-item ${reminder.completed ? 'completed' : ''}`}>
              <div className="reminder-content">
                <h4>{reminder.title}</h4>
                {reminder.description && <p>{reminder.description}</p>}
                <small>Due: {formatDate(reminder.due_date)}</small>
              </div>
              {!reminder.completed && (
                <button 
                  onClick={() => completeReminder(reminder.id)}
                  className="complete-btn"
                >
                  ✓
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
} 