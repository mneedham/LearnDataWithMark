from phi.agent import Agent
from phi.tools.duckdb import DuckDbTools
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.model.openai import OpenAIChat
from phi.run.response import RunEvent, RunResponse

agent = Agent(
    tools=[DuckDbTools()],
    model=OpenAIChat(id="gpt-4o"),
    show_tool_calls=True,
    instructions=[
      """When running select queries, make sure that you put all field names 
      in double quotes to avoid getting syntax errors."
      "e.g. SELECT "column name" FROM "table_name""",
    ],
    add_datetime_to_instructions=True, add_history_to_messages=True,
    storage=SqlAgentStorage(table_name="agent_sessions", db_file="tmp/agent.db"),
)


def as_stream(response):
  for chunk in response:
    if isinstance(chunk, RunResponse) and isinstance(chunk.content, str):
      if chunk.event == RunEvent.run_response:
        yield chunk.content
