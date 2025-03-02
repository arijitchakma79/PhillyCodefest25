import { Box, Button, Input, VStack, HStack, Tabs, Textarea } from "@chakra-ui/react"
import { motion } from "framer-motion";
import { text } from "framer-motion/client";
import { useEffect, useState, useRef } from 'react'


export default function ChatBox () {
	const [messages, setMessages] = useState([]);
	const [input, setInput] = useState("");
	const [typingMessage, setTypingMessage] = useState("");
	const messagesEndRef = useRef(null);

	useEffect(() => {
		// Initial message
		setMessages([{ text: "Hello! How can I assist you today?", sender: "ai" }]);
	  }, []);
  
    const handleSend = async () => {
        if (input.trim() === "") return;
      
        // Add user message to chat
        setMessages([...messages, { text: input, sender: "user" }]);
      
        const userMessage = input;
        setInput("");
      
        try {
          const response = await fetch("http://localhost:3000/api/chat", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ text: userMessage }),
          });
      
          if (!response.ok) {
            throw new Error("Failed to send message");
          }
      
          const data = await response.json();
      
          // Type out AI response
          typeMessage(data.response || "No response from AI");
        } catch (error) {
          console.error("Error:", error);
          typeMessage("Error communicating with server.");
        }
      };
      
      // animates the message typing
	  const typeMessage = async (text) => {
		let tempMessage = "";
		
		setMessages((prevMessages) => [...prevMessages, { text: "", sender: "ai" }]);
	  
		for (let i = 0; i < text.length; i++) {
		  tempMessage += text[i];
	  
		  // Update state less frequently to improve performance (every 3rd character)
		  if (i % 3 === 0 || i === text.length - 1) {
			setMessages((prevMessages) => {
			  const updatedMessages = [...prevMessages];
			  updatedMessages[updatedMessages.length - 1] = { text: tempMessage, sender: "ai" };
			  return updatedMessages;
			});
		  }
	  
		  await new Promise((res) => setTimeout(res, 10)); // Faster speed
		}
	  };
	  
	useEffect(() => {
	  messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
	}, [messages, typingMessage]);
  
	return (
	  <Box maxW="500px" w="100%" borderWidth="1px" borderRadius="md" p={4} bg="white">
		<VStack spacing={4} align="stretch" h="400px">
		  <Box
			flex="1"
			overflowY="auto"
			borderRadius="md"
			p={2}
			h="300px"
		  >
			{messages.map((msg, index) => (
			<motion.div
				key={index}
				initial={{ opacity: 0 }}
				animate={{ opacity: 1 }}
				transition={{ duration: 0.5 }}
				style={{
				display: "flex",
				justifyContent: msg.sender === "user" ? "flex-end" : "flex-start", // Align user to right, AI to left
				}}
			>
				<div
				style={{
					background: msg.sender === "user" ? "#E2E8F0" : "#ffffff", // Blue for user, Gray for AI
					color: "black", //janky
					padding: "8px 12px",
					borderRadius: "12px",
					maxWidth: "75%",
					marginBottom: "8px",
					textAlign: msg.sender === "user" ? "right" : "left", // Right-align user text
				}}
				>
				{msg.text}
				</div>
			</motion.div>
			))}
			{typingMessage && (
			  <motion.div
				initial={{ opacity: 0 }}
				animate={{ opacity: 1 }}
				transition={{ duration: 0.5 }}
				style={{
				  alignSelf: "flex-start",
				  background: "#ffffff",
				  padding: "8px",
				  borderRadius: "8px",
				  maxWidth: "75%",
				  marginBottom: "8px"
				}}
			  >
				{typingMessage}
			  </motion.div>
			)}
			<div ref={messagesEndRef} />
		  </Box>
		  <Box display="flex" gap={2}>
			<Input
			  value={input}
			  onChange={(e) => setInput(e.target.value)}
			  placeholder="Type your message..."
			  flex="1"
			/>
			<Button onClick={handleSend} colorScheme="blue">
			  Send
			</Button>
		  </Box>
		</VStack>
	  </Box>
	);
};