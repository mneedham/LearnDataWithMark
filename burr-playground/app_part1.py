import textwrap, instructor, re, itertools
from burr.core import ApplicationBuilder, State, action, expr
from openai import OpenAI
from models import Video
from rich.console import Console

c = Console()
llm_client = instructor.from_openai(OpenAI())


@action(reads=[], writes=["post", "description"])
def generate_titles(state: State, description: str, llm_client) -> State:
  """Use the Instructor LLM client to generate `Video` from 
     the YouTube video description."""

  prompt = description
  response = llm_client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=Video,
    messages=[
      {
        "role": "system",
        "content": """Analyze the given YouTube video description 
                      and generate a compelling title.""",
      },
      {"role": "user", "content": prompt},
      ],
  )
  return state.update(post=response, description=description)


application = (
  ApplicationBuilder()
  .with_actions(
    generate_titles.bind(llm_client=llm_client)
  )
  .with_transitions()
  .with_entrypoint("generate_titles")
  .build()
)

description = """
Llama 3.2-vision is a multimodal large language model by Meta, 
and it's finally available on Ollama! 
We're going to see how well it performs on a few different tasks: 
extracting code from an image, reading my terrible handwriting, 
and critiquing one of my YouTube thumbnails.
"""

inputs = {"description": description}
action, result, state = application.run(
  halt_before=[],
  halt_after=["generate_titles"],
  inputs=inputs,
)

c.print(f"Action: {action.name}")
for item in state["post"].titles:
  c.print(item)