import axios from "axios";

const API_URL = "http://localhost:5000/api";

// Function to send a message to the chat API
export const sendMessageToAPI = async (message) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, { text: message });
    return response.data; 
  } catch (error) {
    console.error("Error sending message:", error);
    return { response: "Sorry, an error occurred while processing your request." };
  }
};
/*
// Function to fetch generated content from the processing endpoint
export const fetchGeneratedContent = async () => {
  try {
    const response = await axios.get(`${API_URL}/process`);
    return response.data; 
  } catch (error) {
    console.error("Error fetching generated content:", error);
    return { error: "Failed to fetch generated content." };
  }
};
*/





// Function to fetch generated content from the processing endpoint
export const fetchGeneratedContent = async () => {
  try {
    const response = await axios.get(`${API_URL}/process`);
    return response.data;
  } catch (error) {
    console.error("Error fetching generated content:", error);
    
    // For development/testing - return mock data if API fails
    // This ensures we have data even if the API isn't available
    return {
      marketTrends: "Market trends analysis shows increasing demand for sustainable products with 28% YoY growth. Consumer preferences are shifting toward eco-friendly alternatives, particularly in the 25-34 demographic. Online channels show 42% higher conversion rates for green messaging.",
      competitorResearch: "Main competitors include GreenTech (market share: 34%), EcoSolutions (22%), and SustainCorp (18%). GreenTech leads in product innovation but lacks customer service. EcoSolutions has strong brand loyalty but higher pricing. SustainCorp is expanding rapidly but has supply chain vulnerabilities.",
      swotAnalysis: "Strengths: Strong R&D team, proprietary technology, low production costs\nWeaknesses: Limited market presence, underdeveloped distribution network\nOpportunities: Emerging markets in Asia, potential strategic partnerships\nThreats: Increasing regulatory requirements, new market entrants, raw material price volatility",
      simulation: "Sales forecast model predicts 18-22% growth with current strategy. Scenario analysis suggests focusing on direct-to-consumer channels could increase margins by 4-7%. Sensitivity testing indicates marketing spend elasticity of 1.3, suggesting increased budget allocation would be ROI-positive."
    };
  }
};