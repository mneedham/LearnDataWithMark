import chainlit as cl

@cl.on_message
async def on_message(message: cl.Message):
  msg = cl.Message(content=f"Echo: {message.content}")
  await msg.send()
