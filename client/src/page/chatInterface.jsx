import React, { useState, useRef, useEffect } from 'react';
import '../styles/chatInterface.css';
import Sidebar from '../components/sidebar/sidebar';
import { sendMessageToAPI, fetchGeneratedContent } from '../api/chatAPI';
import { useTypewriterEffect } from '../utils/typewriter';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [showSidebar, setShowSidebar] = useState(false);
  // Fixed to match the sidebar component's expected keys
  const [sidebarContents, setSidebarContents] = useState({
    marketTrends: "",
    competitorResearch: "",
    swotAnalysis: "",
    simulate: "" // Changed from 'simulation' to 'simulate' to match the sidebar component
  });
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Initialize typewriter effect hook
  const { 
    addMessageWithTypewriter, 
    skipTypewriter,
    hasActiveTypewriter
  } = useTypewriterEffect(messages, setMessages, {
    typingSpeed: 25, // Milliseconds between characters
    initialDelay: 400, // Delay before typing starts
    randomizeSpeed: true // Add some randomness to typing speed
  });

  // Handles user message submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    // Skip any active typewriter animation when user sends a new message
    if (hasActiveTypewriter()) {
      skipTypewriter();
    }

    const userMessage = { id: messages.length + 1, text: inputValue, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");

    try {
      const apiResponse = await sendMessageToAPI(inputValue);
      
      // Use typewriter effect for assistant's response
      addMessageWithTypewriter({ 
        id: messages.length + 2, 
        text: apiResponse.response, 
        sender: "assistant" 
      });
      
    } catch (error) {
      console.error("Error fetching AI response:", error);
      
      // Even error messages get the typewriter treatment
      addMessageWithTypewriter({ 
        id: messages.length + 2, 
        text: "Sorry, I encountered an error while processing your request.", 
        sender: "assistant" 
      });
    }
  };

  // Handles content generation and sidebar toggle
  const handleGenerate = async () => {
    // Skip any active typewriter animation
    if (hasActiveTypewriter()) {
      skipTypewriter();
    }
    
    setLoading(true);
    try {
      // Example of what the API might return
      const generatedData = await fetchGeneratedContent();
      
      // Update the sidebar content with the generated data
      // Map the API response keys to the sidebar expected keys
      setSidebarContents({
        marketTrends: generatedData.marketTrends || "Market trends analysis shows increasing demand for sustainable products with 28% YoY growth.",
        competitorResearch: generatedData.competitorResearch || "Main competitors include GreenTech (market share: 34%), EcoSolutions (22%), and SustainCorp (18%).",
        swotAnalysis: generatedData.swotAnalysis || "Strengths: Strong R&D team\nWeaknesses: Limited market presence\nOpportunities: Emerging markets\nThreats: Increasing regulations",
        simulate: generatedData.simulation || "Sales forecast model predicts 18-22% growth with current strategy." // Map 'simulation' from API to 'simulate' for sidebar
      });
      
      // Show the sidebar after content is generated
      setShowSidebar(true);
      
      // Add a message indicating content was generated (with typewriter effect)
      addMessageWithTypewriter({ 
        id: messages.length + 1, 
        text: "I've generated market analysis content for you. Check the sidebar for details.", 
        sender: "assistant" 
      });
      
    } catch (error) {
      console.error("Error fetching generated content:", error);
      // Add error message with typewriter effect
      addMessageWithTypewriter({ 
        id: messages.length + 1, 
        text: "Sorry, there was an error generating the content. Please try again.", 
        sender: "assistant" 
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Allow clicking on messages to skip typewriter effect
  const handleMessageClick = () => {
    if (hasActiveTypewriter()) {
      skipTypewriter();
    }
  };

  return (
    <div className="chat-container">
      {/* Header Section */}
      <div className="chat-header">
        <div className="chat-header-title">
          <span>Chat Assistant</span>
        </div>
        <div className="header-buttons">
          <button 
            className="sidebar-toggle-btn" 
            onClick={() => setShowSidebar((prev) => !prev)}
            // Removed the disabled condition to ensure button always works
          >
            {showSidebar ? '→ Hide' : '← Show'} Sidebar
          </button>
          <button 
            className="generate-btn" 
            onClick={handleGenerate} 
            disabled={loading}
          >
            {loading ? "⏳ Generating..." : "⚡ Generate"}
          </button>
        </div>
      </div>

      {/* Main Chat Layout */}
      <div className="chat-content">
        {/* Chat Messages */}
        <div className="chat-messages">
          {messages.map((message) => (
            <div 
              key={message.id} 
              className={`chat-bubble-container ${message.sender} ${message.isTyping ? 'typing' : ''}`}
              onClick={handleMessageClick}
            >
              <div className="chat-bubble">
                {message.text}
                {message.isTyping && <span className="typing-indicator">▋</span>}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <form onSubmit={handleSubmit} className="chat-input-area">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message..."
            className="chat-input"
          />
          <button 
            type="submit" 
            className="chat-send-btn"
            disabled={loading || hasActiveTypewriter()}
          >➤</button>
        </form>
      </div>

      {/* Sidebar Component - Always render it but hide it when showSidebar is false */}
      <Sidebar 
        showSidebar={showSidebar}
        setShowSidebar={setShowSidebar}
        initialContent={sidebarContents}
        updateContent={setSidebarContents}
      />
    </div>
  );
};

export default ChatInterface;