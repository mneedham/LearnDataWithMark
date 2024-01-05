import chainlit as cl
import litellm

@cl.on_message
async def on_message(message: cl.Message):
  msg = cl.Message(content="")
  await msg.send()

  system_message = {
    "role": "system", 
    "content": "You are a helpful assistant who tries their best to answer questions."
  }

  response = await litellm.acompletion(
    model="ollama/mixtral",
    messages = [
      system_message,
      {"role": "user", "content": message.content}
    ],
    api_base="http://localhost:11434",
    stream=True
  )

  async for chunk in response:
    if chunk:
      content = chunk.choices[0].delta.content
      if content:
        await msg.stream_token(content)

  await msg.update()
