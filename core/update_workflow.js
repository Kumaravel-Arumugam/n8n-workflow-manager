import axios from "axios";
import fs from "fs";
import dotenv from "dotenv";

dotenv.config({ path: '../.env' });

const N8N_API_KEY = process.env.N8N_API_KEY;
const N8N_BASE_URL = process.env.N8N_BASE_URL;
const WORKFLOW_ID = "GDeQD6XpAGoHASTo";

const client = axios.create({
  baseURL: N8N_BASE_URL,
  headers: {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json",
  },
});

async function updateWorkflow() {
  try {
    const workflowJson = JSON.parse(fs.readFileSync('../projects/job-market-analysis/workflow.json', 'utf8'));
    console.log("Updating workflow:", workflowJson.name);
    
    // Remove fields that can't be updated
    delete workflowJson.id;
    delete workflowJson.createdAt;
    delete workflowJson.updatedAt;
    delete workflowJson.versionId;
    
    const response = await client.put(`/api/v1/workflows/${WORKFLOW_ID}`, workflowJson);
    console.log("Success! Updated workflow ID:", response.data.id);
    console.log("Version:", response.data.versionId);
  } catch (error) {
    console.error("Update failed:", error.message);
    if (error.response) {
      console.error("Status:", error.response.status);
      console.error("Data:", JSON.stringify(error.response.data, null, 2));
    }
  }
}

updateWorkflow();
