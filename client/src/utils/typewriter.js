
export const typewriterEffect = (text, onUpdate, onComplete, options = {}) => {
  const {
    typingSpeed = 30,
    initialDelay = 300,
    randomizeSpeed = true
  } = options;
  
  let currentIndex = 0;
  let timeoutId = null;
  let stopped = false;
  
  // Start the typewriter effect
  const start = () => {
    if (stopped) return;
    
    // Initial delay before starting to type
    timeoutId = setTimeout(() => {
      typeNextCharacter();
    }, initialDelay);
  };
  
  // Type the next character
  const typeNextCharacter = () => {
    if (stopped) return;
    
    if (currentIndex <= text.length) {
      const currentText = text.substring(0, currentIndex);
      onUpdate(currentText);
      currentIndex++;
      
      // Calculate delay for next character
      let delay = typingSpeed;
      if (randomizeSpeed) {
        // Add some randomness to make it feel more natural
        delay = typingSpeed * (0.7 + Math.random() * 0.6);
      }
      
      // Add slightly longer pauses for punctuation
      const lastChar = currentText[currentText.length - 1];
      if (['.', '!', '?', ',', ';', ':'].includes(lastChar)) {
        delay *= 2;
      }
      
      if (currentIndex <= text.length) {
        timeoutId = setTimeout(typeNextCharacter, delay);
      } else {
        // Typing is complete
        if (onComplete) onComplete();
      }
    }
  };
  
  // Stop the typewriter effect
  const stop = () => {
    stopped = true;
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    // Immediately show full text when stopped
    onUpdate(text);
    if (onComplete) onComplete();
  };
  
  return {
    start,
    stop
  };
};

/**
 * Hook for adding typewriter effect to chat messages
 * @param {Array} messages - Array of chat messages
 * @param {function} setMessages - Function to update messages state
 * @param {object} options - Configuration options for typewriter effect
 * @returns {object} - Methods to manage typewriter effect
 */
export const useTypewriterEffect = (messages, setMessages, options = {}) => {
  let activeTypewriter = null;
  
  /**
   * Add a new message with typewriter effect
   * @param {object} message - Message object to add
   */
  const addMessageWithTypewriter = (message) => {
    // If message is not from assistant, just add it normally
    if (message.sender !== 'assistant') {
      setMessages(prev => [...prev, message]);
      return;
    }
    
    // For assistant messages, start with empty text
    const initialMessage = {
      ...message,
      text: '',
      isTyping: true
    };
    
    setMessages(prev => [...prev, initialMessage]);
    
    // Create typewriter effect
    const originalText = message.text;
    activeTypewriter = typewriterEffect(
      originalText,
      // Update function
      (currentText) => {
        setMessages(prev => {
          const newMessages = [...prev];
          // Find the message we're currently typing
          const lastIndex = newMessages.length - 1;
          newMessages[lastIndex] = {
            ...newMessages[lastIndex],
            text: currentText
          };
          return newMessages;
        });
      },
      // Complete function
      () => {
        setMessages(prev => {
          const newMessages = [...prev];
          const lastIndex = newMessages.length - 1;
          newMessages[lastIndex] = {
            ...newMessages[lastIndex],
            isTyping: false
          };
          return newMessages;
        });
        activeTypewriter = null;
      },
      options
    );
    
    activeTypewriter.start();
  };
  
  /**
   * Skip the current typewriter animation
   */
  const skipTypewriter = () => {
    if (activeTypewriter) {
      activeTypewriter.stop();
    }
  };
  
  return {
    addMessageWithTypewriter,
    skipTypewriter,
    hasActiveTypewriter: () => activeTypewriter !== null
  };
};