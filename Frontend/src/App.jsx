import { useEffect, useState } from 'react'
import './App.css'
import ThinkingTreeChart from './ThinkingTreeChart'

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
	  <ThinkingTreeChart/>
    </>
  )
}