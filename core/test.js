import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

// Configuration from index.js
const N8N_API_KEY = process.env.N8N_API_KEY;
const N8N_BASE_URL = process.env.N8N_BASE_URL;

const client = axios.create({
  baseURL: N8N_BASE_URL,
  headers: {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json",
  },
});

async function testConnection() {
  try {
    console.log("Testing connection to n8n...");
    const response = await client.get("/api/v1/workflows?limit=5");
    console.log("Success! Found workflows:", response.data.data.length);
    console.log("First workflow name:", response.data.data[0]?.name);
  } catch (error) {
    console.error("Connection failed:", error.message);
    if (error.response) {
      console.error("Status:", error.response.status);
      console.error("Data:", JSON.stringify(error.response.data));
    }
  }
}

testConnection();
