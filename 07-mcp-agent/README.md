# 07 - MCP Agent

Build an AI agent that uses tools via the Model Context Protocol

## What You'll Learn

- The Model Context Protocol (MCP) specification
- Building an MCP server with stdio transport
- Building an MCP client that communicates via JSON-RPC
- Connecting AI agents to standardized tool interfaces

## Architecture

```mermaid
graph TD
    UserQuery[User Query] --> Agent[Agent (main.py)]
    Agent --> MCPClient[MCP Client (mcp_client.py)]
    MCPClient -- "JSON-RPC (stdio)" --> MCPServer[MCP Server (mcp_server.py)]
    MCPServer --> ToolExecution[Tool Execution]
    ToolExecution --> MCPServer
    MCPServer -- Result --> MCPClient
    MCPClient --> Agent
    Agent --> Answer[Answer]
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## How It Works

This project implements a 3-file architecture to demonstrate the Model Context Protocol:

- **main.py (Agent):** The entry point that orchestrates the AI agent, manages user interaction, and utilizes the MCP client to access tools.
- **mcp_client.py (Client):** Implements the client-side logic of the MCP, handling JSON-RPC communication over stdio with the server.
- **mcp_server.py (Server):** Defines the tools available to the agent and executes them when requested by the client.

## Key Concepts

- **MCP:** Model Context Protocol, an open standard that enables AI models to interact with external data and tools.
- **JSON-RPC 2.0:** A lightweight remote procedure call protocol used for communication between the client and server.
- **stdio transport:** Uses standard input/output streams as the communication channel between the MCP client and server.
- **Tool Schemas:** Definitions that describe available tools, their parameters, and return types in a format models can understand.
- **Client-Server Architecture:** Decoupling the AI agent from the tool execution environment for better scalability and security.

## What is MCP?

The Model Context Protocol (MCP) is a standard launched in late 2024 to solve the fragmentation in how AI agents connect to data sources and tools. In 2025 and 2026, it has become the industry standard, allowing developers to build tool providers (servers) once and use them across any AI agent (client) that supports the protocol, eliminating the need for custom integrations for every new tool.
