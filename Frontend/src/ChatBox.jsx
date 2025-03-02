import { Box, Button, Input, VStack, HStack, Tabs, Textarea } from "@chakra-ui/react"
import { motion } from "framer-motion";
import { useEffect, useState, useRef } from 'react'


export default function ChatBox () {
	const [messages, setMessages] = useState([]);
	const [input, setInput] = useState("");
	const [typingMessage, setTypingMessage] = useState("");
	const messagesEndRef = useRef(null);
  
	const handleSend = () => {
	  if (input.trim() === "") return;
	  setMessages([...messages, { text: input, sender: "user" }]);
	  setInput("");
	  
	  setTimeout(() => {
		typeMessage("This is a response from AI");
	  }, 500);
	};
  
	const typeMessage = (text) => {
	  setTypingMessage("");
	  let index = 0;
	  const interval = setInterval(() => {
		if (index < text.length) {
		  setTypingMessage((prev) => prev + text[index]);
		  index++;
		} else {
		  clearInterval(interval);
		  setMessages((prev) => [...prev, { text, sender: "ai" }]);
		  setTypingMessage("");
		}
	  }, 50);
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
				  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
				  background: msg.sender === "user" ? "#f1f1f1" : "#ffffff",
				  padding: "8px",
				  borderRadius: "8px",
				  maxWidth: "75%",
				  marginBottom: "8px"
				}}
			  >
				{msg.text}
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