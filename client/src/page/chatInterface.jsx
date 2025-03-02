import React, { useState, useRef, useEffect } from 'react';
import '../styles/chatInterface.css';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you today?", sender: "assistant" },
    { id: 2, text: "This is an example of a longer message that will wrap to the next line because it exceeds the maximum width we've set for messages.", sender: "assistant" }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [showSidebar, setShowSidebar] = useState(false);
  const [sidebarContent, setSidebarContent] = useState("");
  const messagesEndRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() === "") return;
    
    const newMessage = { id: messages.length + 1, text: inputValue, sender: "user" };
    setMessages([...messages, newMessage]);
    setInputValue("");
    
    setTimeout(() => {
      const assistantResponses = [
        "I'm here to help! What would you like to know?",
        "That's an interesting question. Let me think about it.",
        "I understand what you're asking. Here's what I know.",
        "Thank you for sharing that with me.",
        "Could you provide more details about your question?"
      ];
      
      const randomResponse = assistantResponses[Math.floor(Math.random() * assistantResponses.length)];
      setMessages(prev => [...prev, { id: prev.length + 1, text: randomResponse, sender: "assistant" }]);
    }, 1000);
  };

  const handleGenerate = () => {
    const codeExamples = [
      `function greet() {\n  console.log("Hello, world!");\n}\n\ngreet();`,
      `def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))`,
      `import React from 'react';\n\nconst App = () => {\n  return <h1>Hello React!</h1>;\n};\n\nexport default App;`,
      `SELECT name, age \nFROM users \nWHERE age > 21 \nORDER BY name ASC;`
    ];
    
    const randomCode = codeExamples[Math.floor(Math.random() * codeExamples.length)];
    setSidebarContent(randomCode);
    setShowSidebar(true);
  };

  const toggleSidebar = () => {
    if (!showSidebar) {
      // If sidebar is not showing, generate content first
      handleGenerate();
    } else {
      // If sidebar is showing, just toggle it off
      setShowSidebar(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-container">
      {/* Header */}
      <div className="chat-header">
        <div className="chat-header-title">
          <div className="chat-status-indicator"></div>
          <span>Chat Interface</span>
        </div>
        <div className="header-buttons">
          <button 
            className="sidebar-toggle-btn"
            onClick={toggleSidebar}
            aria-label="Toggle sidebar"
          >
            {showSidebar ? '→' : '←'}
          </button>
          <button className="chat-settings-btn" aria-label="Settings">⚙️</button>
        </div>
      </div>
      
      {/* Messages area */}
      <div className="chat-messages">
        {messages.map(message => (
          <div key={message.id} className={`chat-bubble-container ${message.sender}`}>
            <div className="chat-bubble">{message.text}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input area */}
      <form onSubmit={handleSubmit} className="chat-input-area">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Type a message..."
          className="chat-input"
        />
        <button type="submit" className="chat-send-btn" aria-label="Send message">➤</button>
        <button 
          type="button" 
          onClick={handleGenerate} 
          className="chat-generate-btn"
          aria-label="Generate content"
        >⚡</button>
      </form>
      
      {/* Sidebar for Generated Content */}
      {showSidebar && (
        <div className="sidebar">
          <div className="sidebar-header">
            <h3>Generated Content</h3>
            <button 
              onClick={() => setShowSidebar(false)} 
              className="sidebar-close"
              aria-label="Close sidebar"
            >✕</button>
          </div>
          <div className="sidebar-content">
            <pre>{sidebarContent}</pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;