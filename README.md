# 🧠 Wikipedia Agent with LangGraph + MCP

This project implements a conversational AI agent that uses LangGraph and the MCP (Model Context Protocol) to search Wikipedia and return information using a tool-based architecture. It demonstrates multi-turn interactions with tool calling, Wikipedia queries, and LangChain tool composition.

---

## 📦 Features

- 🔍 Search Wikipedia for summaries and page links
- 📚 List all section titles of a given Wikipedia topic
- 📄 Fetch specific section content from a topic
- 🔁 Uses LangGraph for graph-based tool routing
- 🤖 Powered by OpenAI GPT-4 with tool bindings
- 🧩 MCP server supports composable, stateless tool APIs over `stdio`

---

## 🛠️ Technologies Used

- Python 3.10+
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain OpenAI](https://python.langchain.com/docs/integrations/llms/openai/)
- [FastMCP](https://pypi.org/project/mcp/)
- [Wikipedia Python API](https://pypi.org/project/wikipedia/)
- OpenAI GPT-4 API

---

## 🚀 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/wikipedia-mcp-agent.git
cd wikipedia-mcp-agent
