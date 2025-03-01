from src.llm_agent import LLMAgent, OutputFormat


class TestAgent(LLMAgent):
    def __init__(self, output_format=OutputFormat.TEXT):
        instructions = """You are a helpful travel assistant. 
Your role is to help users plan their trips, suggest destinations, and provide travel tips."""
        
        knowledge = """
Popular destinations:
1. Paris, France - Known for the Eiffel Tower, Louvre Museum, and exquisite cuisine.
2. Tokyo, Japan - A blend of traditional culture and modern technology.
3. New York City, USA - The city that never sleeps, featuring Broadway, Central Park, and the Statue of Liberty.
4. Bali, Indonesia - Beautiful beaches, vibrant culture, and spiritual temples.
5. Rome, Italy - Historical sites including the Colosseum, Roman Forum, and Vatican City.

Travel seasons:
- High season: June to August (Summer in Northern Hemisphere)
- Shoulder season: April-May and September-October
- Low season: November to March (except for holiday weeks)

Budget considerations:
- Budget travel: $50-100 per day
- Mid-range travel: $100-300 per day
- Luxury travel: $300+ per day
"""
        
        super().__init__(
            instructions=instructions,
            output_format=output_format,
            knowledge=knowledge,
            store_history=True
        )
        
        # Add examples for few-shot learning
        self.add_example("user", "I want to visit Europe in the summer. Where should I go?")
        self.add_example("assistant", """I'd recommend visiting Paris, France during the summer!

Paris is beautiful in summer, though it's high season (June-August) so expect more tourists and higher prices. The weather is pleasant, typically 15-25°C (59-77°F), perfect for exploring.

Key attractions include:
- Eiffel Tower
- Louvre Museum
- Notre-Dame Cathedral
- Seine River cruises
- Montmartre district

Since it's high season, book accommodations and major attractions in advance. Consider day trips to Versailles Palace or the Loire Valley.

Would you like more specific recommendations based on your interests or budget?""")
