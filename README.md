# AI Agent & Prompt Engineering Portfolio Demo

This repository demonstrates practical skills in building AI agents, designing multi-step reasoning workflows, integrating tool calling, and evaluating prompts. It utilizes both OpenAI's API for intelligent routing and HuggingFace pipelines for multimodal tasks.

## Features

- **Tool-Calling Agent**: A from-scratch ReAct-style agent utilizing OpenAI's tool-calling API to handle multi-step user queries.
- **Multimodal Capabilities**: Integration with HuggingFace (`transformers`) to process and caption images on the fly.
- **Prompt Benchmarking**: Scripts to evaluate agent reasoning and tool-calling success rates across different system prompt variations.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables:
   Copy `.env.example` to `.env` and fill in your `OPENAI_API_KEY` and `HF_TOKEN`.

## Running the Demo

- Run the interactive agent:
  ```bash
  python agent.py
  ```
- Run the prompt evaluation benchmark:
  ```bash
  python evaluate.py
  ```
