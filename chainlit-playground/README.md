# Building a chatbot with Chainlit

In this video, we'll learn how to build a mini ChatGPT that runs on our machine using Mixtral, Ollama, llmlite, and Chainlit. We'll build it up from scratch, starting with a chatbot that echos back messages, before moving onto one that remembers the chat history and using Mixtral to answer questions. And finally, we'll add functionality that lets the chatbot answer questions on uploaded text files.

You can see the code of the steps up to the final solution:

* [chat_echo.py](chat_echo-py) - Echos any messages you send.

Set up a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/active
```

Install dependencies

```bash
pip install chainlit litellm
```

Run the chatbot:

```bash
chainlit run chat.py -w -h
```

Navigate to http://localhost:8000

Watch the video

[![Constraining LLMs with Guidance AI](https://img.youtube.com/vi/4Wz61w5zbCk/0.jpg)](https://www.youtube.com/watch?v=4Wz61w5zbCk "Constraining LLMs with Guidance AI")
