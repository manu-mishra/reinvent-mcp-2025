#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { loadSessions } from './data/loader.js';
import { createSessionTools } from './tools/sessionTools.js';

const server = new Server(
  {
    name: 'reinvent-2025-mcp',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

let tools = {};

// Load data and initialize tools
async function initialize() {
  const sessions = await loadSessions();
  tools = createSessionTools(sessions);
  // Debug output removed for MCP compatibility
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: Object.values(tools).map(tool => ({
    name: tool.name,
    description: tool.description,
    inputSchema: tool.inputSchema
  }))
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (!tools[name]) {
    throw new Error(`Tool ${name} not found`);
  }
  
  const result = await tools[name].handler(args);
  
  return {
    content: [
      {
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }
    ]
  };
});

async function main() {
  await initialize();
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
