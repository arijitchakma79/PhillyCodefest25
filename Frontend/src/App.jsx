import { useEffect, useState } from 'react'
import './App.css'
import ThinkingTreeChart from './ThinkingTreeChart'

import { Textarea } from "@chakra-ui/react"
import { HStack } from "@chakra-ui/react"
import { Tabs } from "@chakra-ui/react"

const ChatBox = () => {
	return <Textarea placeholder="Comment..." />
}

const TabBox = () => {
	return (
	  <Tabs.Root defaultValue="thinking">
		<Tabs.List>
		  <Tabs.Trigger value="thinking">
			Thinking
		  </Tabs.Trigger>
		  <Tabs.Trigger value="graphs">
			Graphs
		  </Tabs.Trigger>
		  <Tabs.Trigger value="swot">
			SWOT
		  </Tabs.Trigger>
		  <Tabs.Trigger value="business">
			Business
		  </Tabs.Trigger>
		  <Tabs.Trigger value="market">
			Market
		  </Tabs.Trigger>
		</Tabs.List>

		<Tabs.Content value="thinking">
			Live thinking tree of the agents 
			<ThinkingTreeChart/>
		</Tabs.Content>
		<Tabs.Content value="graphs">Graphs</Tabs.Content>
		<Tabs.Content value="swot">Strengths, Weaknesses, Opporunity, and Threats Analysis</Tabs.Content>
		<Tabs.Content value="business">Business Documents</Tabs.Content>
		<Tabs.Content value="market">Market Analysis</Tabs.Content>

	  </Tabs.Root>
	)
  }

  

export default function App() {
  const [count, setCount] = useState(0)
  	
  //useEffect(() => {alert("Wake up!")}, [count]);
  

  return (
    <>
      <h1>VentureAhead</h1>
      <p className="text">
        A Multi-agent solution for startup and business simulation, market and competitor analysis, and ...
      </p>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          Generate {count}
        </button>
      </div>
	  <HStack>
		<ChatBox h="20" />
		<TabBox h="20" />
	  </HStack>
    </>
  )
}