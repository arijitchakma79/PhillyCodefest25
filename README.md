# VentureAhead

VentureAhead is a web-application built for entrepreneurs and anyone looking to 
simulate analysis for business feasibility. It coordinates multiple AI-agents to
reason about different aspects of the communicated business idea including:
- Business Information
- Business Simulation - the possible future steps for the business 
- Market Information
- Competitors
- SWOT Analysis (Strength, Weakness, Opportunities, Threats)
- Graphs (revenue growth)

The two clusters of AI agents:
- Data Research Agents  
  - Perplexity API
  - GoogleTrends API
- Thinking & Reasoning Agents
  -  Business Simulation and Future Steps
  -  Ideation Processing Feedback

# Overview

## Ideation
1. User chats with ChatBot to share information about the user's business idea.
2. Click `Generate` to process the collected user information.

## Processing
4. AI researches data about idea.
5. AI reasons about future steps.

## Feedback
6. Display collected data and reasoning and different tabs.

# How to Use
Install the dependencies using the following command: 

`pip install -r requirements.txt`

## To Run the Servers 
### (ThinkingServer and ResearchServer)
```
cd server/
build go
./server
cd ..
```


Group Members: 
- Eray Aktokluk
- Arijit Chakma
- Safa Obuz
- Krisi Hristova 
