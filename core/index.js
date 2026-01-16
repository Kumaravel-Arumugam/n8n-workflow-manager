import dotenv from "dotenv";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import axios from "axios";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

// Get directory path for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load .env from parent directory (relative path, works for any user)
dotenv.config({ path: join(__dirname, "..", ".env") });

// Configuration
const N8N_API_KEY = process.env.N8N_API_KEY;
const N8N_BASE_URL = process.env.N8N_BASE_URL;

const client = axios.create({
  baseURL: N8N_BASE_URL,
  headers: {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json",
  },
});

const server = new Server(
  {
    name: "n8n-manager",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "n8n_create_workflow",
        description: "Create a new n8n workflow",
        inputSchema: {
          type: "object",
          properties: {
            name: { type: "string", description: "Name of the workflow" },
            nodes: {
              type: "array",
              description: "Array of workflow nodes",
              items: { type: "object" },
            },
            connections: {
              type: "object",
              description: "Workflow connections object",
            },
            tags: {
              type: "array",
              description: "Array of tag names to apply",
              items: { type: "string" },
            },
          },
          required: ["name", "nodes", "connections"],
        },
      },
      {
        name: "n8n_update_workflow",
        description: "Update an existing n8n workflow",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Workflow ID" },
            name: { type: "string", description: "Name of the workflow" },
            nodes: {
              type: "array",
              description: "Array of workflow nodes",
              items: { type: "object" },
            },
            connections: {
              type: "object",
              description: "Workflow connections object",
            },
          },
          required: ["id", "nodes", "connections"],
        },
      },
      {
        name: "n8n_get_workflow",
        description: "Get details of a specific workflow",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Workflow ID" },
          },
          required: ["id"],
        },
      },
      {
        name: "n8n_list_workflows",
        description: "List all workflows to find IDs",
        inputSchema: {
          type: "object",
          properties: {
            limit: { type: "number", description: "Max results", default: 50 },
          },
        },
      },
      {
        name: "n8n_activate_workflow",
        description: "Activate or deactivate a workflow",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Workflow ID" },
            active: { type: "boolean", description: "True to activate, false to deactivate" },
          },
          required: ["id", "active"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    switch (request.params.name) {
      case "n8n_create_workflow": {
        const { name, nodes, connections, tags } = request.params.arguments;
        // Basic payload
        const payload = { name, nodes, connections };
        if (tags) payload.tags = tags;
        
        const response = await client.post("/api/v1/workflows", payload);
        return {
          content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
        };
      }

      case "n8n_update_workflow": {
        const { id, name, nodes, connections } = request.params.arguments;
        const payload = { nodes, connections };
        if (name) payload.name = name; // Update name if provided

        const response = await client.put(`/api/v1/workflows/${id}`, payload);
        return {
          content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
        };
      }

      case "n8n_get_workflow": {
        const { id } = request.params.arguments;
        const response = await client.get(`/api/v1/workflows/${id}`);
        return {
          content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
        };
      }

      case "n8n_list_workflows": {
         const limit = request.params.arguments?.limit || 50;
         const response = await client.get(`/api/v1/workflows?limit=${limit}`);
         // Simplify output for LLM consumption
         const simplified = response.data.data.map(w => ({
            id: w.id,
            name: w.name,
            active: w.active
         }));
         return {
           content: [{ type: "text", text: JSON.stringify(simplified, null, 2) }],
         };
      }
      
      case "n8n_activate_workflow": {
        const { id, active } = request.params.arguments;
        const response = await client.post(`/api/v1/workflows/${id}/${active ? 'activate' : 'deactivate'}`);
        return {
           content: [{ type: "text", text: JSON.stringify(response.data, null, 2) }],
        };
      }

      default:
        throw new Error("Unknown tool");
    }
  } catch (error) {
    const errorMessage = error.response?.data?.message || error.message;
    const errorDetails = error.response?.data ? JSON.stringify(error.response.data) : "";
    return {
      content: [{ type: "text", text: `Error: ${errorMessage} ${errorDetails}` }],
      isError: true,
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
