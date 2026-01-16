import axios from "axios";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config();

const N8N_API_KEY = process.env.N8N_API_KEY;
const N8N_BASE_URL = process.env.N8N_BASE_URL;

const client = axios.create({
  baseURL: N8N_BASE_URL,
  headers: {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json",
  },
});

async function uploadWorkflow() {
  try {
    const workflowJson = JSON.parse(fs.readFileSync('analysis_workflow.json', 'utf8'));
    console.log("Uploading workflow:", workflowJson.name);
    
    const response = await client.post("/api/v1/workflows", workflowJson);
    console.log("Success! Workflow ID:", response.data.id);
    console.log("Workflow Name:", response.data.name);
    fs.writeFileSync('create_result.json', JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error("Upload failed:", error.message);
    if (error.response) {
      console.error("Status:", error.response.status);
      console.error("Data:", JSON.stringify(error.response.data, null, 2));
    }
  }
}

uploadWorkflow();
