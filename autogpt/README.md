### AutoGPT
  * Importing agents - download the JSON file and import to AutoGPT dashboard and use the agent.

  * Running AutoGPT with Ollama
    - Setup ollama to run on 0.0.0.0:11434 - checkout specific steps for different machines
    - Set the environment variable OLLAMA\_HOST in bashrc (or other similar file)
    - Download the relevant ollama models, eg, llama3
    - In the .env file inside the autogpt\_platform/ directory in autogpt repository, set the following -
      - `OLLAMA_HOST=<your ipv4 address>:11434`
      - `OPENAI_API_BASE_URL=172.17.0.1:11434`
    - In the agent UI advanced options, set Ollama Host = `172.17.0.1:11434`
    - In the autoGPT codebase, change this file - `autogpt_platform/backend/backend/util/request.py`
      - Set `BLOCKED_IP_NETWORKS = []`
    - Rebuild the docker image after the above code change - docker compose up -d --build

  * Testing Ollama
    - Login to the rest service container and run the following -
      - `curl -X POST http://172.17.0.1:11434/api/chat -d '{"messages": [{"role": "user", "content": "what is the capital of India?"}], "stream": false, "model": "llama3"}'`
    - Test from localhost -
      - `curl -X POST http://localhost:11434/api/chat -d '{"messages": [{"role": "user", "content": "what is the capital of India?"}], "stream": false, "model": "llama3"}'`

  * Custom Block Which Also Traces Ollama Calls Using LangFuse
