import axios from "axios";

const API_URL = "http://localhost:3001/api";

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

// Function to fetch generated content from the processing endpoint
export const fetchGeneratedContent = async () => {
  try {
    const response = await axios.get(`${API_URL}/process`);
    console.log(response.data)
    return response.data; 
  } catch (error) {
    console.error("Error fetching generated content:", error);
    return { error: "Failed to fetch generated content." };
  }
};




