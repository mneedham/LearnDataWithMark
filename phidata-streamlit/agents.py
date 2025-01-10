from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from phi.run.response import RunEvent, RunResponse

agent = Agent(
  model=OpenAIChat(model="gpt-4o"),
  tools=[DuckDuckGo(), Newspaper4k()],
  description="You are a researcher writing an article on a topic.",
  instructions=[
    "For a given topic, search for the top 5 links.",
    "Then read each URL and extract the article text.",
    "Analyse and prepare 3-5 bullet points based on the information.",
  ],
  markdown=True, show_tool_calls=True,
  add_datetime_to_instructions=True, add_history_to_messages=True,
  storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent.db"),
)

def as_stream(response):
  for chunk in response:
    if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
      if chunk.event == RunEvent.run_response:
        yield chunk.content
