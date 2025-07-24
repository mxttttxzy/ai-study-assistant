import React, { useState, useEffect } from 'react';
import './AISettings.css';

export default function AISettings({ isOpen, onClose, token }) {
  const [availableModels, setAvailableModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [userPreferences, setUserPreferences] = useState({
    communication_style: 'neutral',
    study_level: 'high_school',
    preferences: {}
  });
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      loadSettings();
    }
  }, [isOpen]);

  const loadSettings = async () => {
    try {
      setLoading(true);
      
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      
      // Load available models
      const modelsResponse = await fetch(`${backendUrl}/api/models`);
      const modelsData = await modelsResponse.json();
      setAvailableModels(modelsData.available_models);
      setSelectedModel(modelsData.default_model);

      // Load user preferences only if logged in
      if (token) {
        const prefsResponse = await fetch(`${backendUrl}/api/user/preferences`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (prefsResponse.ok) {
          const prefsData = await prefsResponse.json();
          setUserPreferences(prefsData);
        }
        // Load user documents
        const docsResponse = await fetch(`${backendUrl}/api/documents`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (docsResponse.ok) {
          const docsData = await docsResponse.json();
          setDocuments(docsData);
        }
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      const content = await readFileContent(file);
      
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/documents/upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          filename: file.name,
          content: content,
          file_type: file.type || 'text/plain'
        })
      });

      if (response.ok) {
        await loadSettings(); // Reload documents
      } else {
        alert('Failed to upload document');
      }
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error uploading document');
    } finally {
      setUploading(false);
    }
  };

  const readFileContent = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target.result);
      reader.onerror = reject;
      reader.readAsText(file);
    });
  };

  const updatePreferences = async () => {
    if (!token) return;
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
      const response = await fetch(`${backendUrl}/api/user/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(userPreferences)
      });
      if (response.ok) {
        alert('Preferences updated successfully!');
      } else {
        const data = await response.json();
        alert(data.detail || 'Failed to update preferences');
      }
    } catch (error) {
      console.error('Error updating preferences:', error);
      alert('Error updating preferences');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="ai-settings-overlay">
      <div className="ai-settings-modal">
        <div className="ai-settings-header">
          <h2>AI Assistant Settings</h2>
          <button onClick={onClose} className="close-btn">×</button>
        </div>
        {loading ? (
          <div className="loading">Loading settings...</div>
        ) : !token ? (
          <div className="ai-settings-content">
            <div className="setting-section">
              <h3>Login Required</h3>
              <p className="setting-description">Please log in to save your preferences and upload documents.</p>
            </div>
          </div>
        ) : (
          <div className="ai-settings-content">
            {/* AI Model Selection */}
            <div className="setting-section">
              <h3>AI Model</h3>
              <select 
                value={selectedModel} 
                onChange={(e) => setSelectedModel(e.target.value)}
                className="model-select"
              >
                <option value="huggingface-free">🤗 HuggingFace Free - Best for general use</option>
                <option value="community-free">🌐 Community Models - Alternative free option</option>
                <option value="ollama-local">🖥️ Ollama Local - Fastest (requires local setup)</option>
                <option value="fallback-enhanced">💡 Enhanced Local - Always available</option>
              </select>
              <p className="setting-description">
                All models are completely free! Choose based on your needs:
                <br/>• <strong>HuggingFace Free:</strong> Best quality, requires internet
                <br/>• <strong>Community Models:</strong> Alternative free option
                <br/>• <strong>Ollama Local:</strong> Fastest, runs on your computer
                <br/>• <strong>Enhanced Local:</strong> Always works, no internet needed
              </p>
            </div>

            {/* Communication Style */}
            <div className="setting-section">
              <h3>Communication Style</h3>
              <select 
                value={userPreferences.communication_style}
                onChange={(e) => setUserPreferences(prev => ({
                  ...prev,
                  communication_style: e.target.value
                }))}
                className="style-select"
              >
                <option value="formal">Formal</option>
                <option value="neutral">Neutral</option>
                <option value="casual">Casual</option>
              </select>
              <p className="setting-description">
                How would you like the AI to communicate with you?
              </p>
            </div>

            {/* Study Level */}
            <div className="setting-section">
              <h3>Study Level</h3>
              <select 
                value={userPreferences.study_level}
                onChange={(e) => setUserPreferences(prev => ({
                  ...prev,
                  study_level: e.target.value
                }))}
                className="level-select"
              >
                <option value="high_school">High School</option>
                <option value="university">University</option>
                <option value="graduate">Graduate</option>
              </select>
              <p className="setting-description">
                Your current academic level helps the AI provide more relevant advice.
              </p>
            </div>

            {/* Document Upload */}
            <div className="setting-section">
              <h3>Upload Documents</h3>
              <div className="file-upload">
                <input
                  type="file"
                  onChange={handleFileUpload}
                  accept=".txt,.pdf,.doc,.docx"
                  disabled={uploading}
                  className="file-input"
                />
                {uploading && <span className="uploading">Uploading...</span>}
              </div>
              <p className="setting-description">
                Upload study materials for the AI to reference in conversations.
              </p>

              {/* Document List */}
              {documents.length > 0 && (
                <div className="documents-list">
                  <h4>Your Documents</h4>
                  {documents.map(doc => (
                    <div key={doc.id} className="document-item">
                      <span className="doc-name">{doc.filename}</span>
                      <span className="doc-date">
                        {new Date(doc.uploaded_at).toLocaleDateString()}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Save Button */}
            <div className="setting-actions">
              <button onClick={updatePreferences} className="save-btn">
                Save Preferences
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 