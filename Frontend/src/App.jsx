import { useEffect, useState, useRef } from 'react'
import './App.css'
import TabBox from './TabBox.jsx'
import ChatBox from './ChatBox.jsx'

import { Box, Button, Input, VStack, HStack, Tabs, Textarea } from "@chakra-ui/react"
import { motion } from "framer-motion";

export default function App() {
  const [count, setCount] = useState(0)
  	
  //useEffect(() => {alert("Wake up!")}, [count]);
  const handleGenerate = async() => {
    try {
      const response = await fetch("http://localhost:3000/api/process", {
        method: "GET",
      });
  
      if (!response.ok) {
        throw new Error("Failed to send GET processing request.");
      }
  
      const data = await response.json();
      console.log(data || "No response received");
      
      // Type out AI response
    } catch (error) {
      console.error("Error:", error);
    }
  }

  return (
    <>
      <h1>VentureAhead</h1>
      <p className="text">
        A Multi-agent solution for startup and business simulation, market and competitor analysis, and ...
      </p>
      <div className="card">
        <button onClick={() => handleGenerate()}>
          Generate
        </button>
      </div>
	  <HStack>
		  <ChatBox h="20" />
		  <TabBox h="20" />
	  </HStack>
    </>
  )
}