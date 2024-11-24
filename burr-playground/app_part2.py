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


@action(reads=["post"], writes=["favourites"])
def select_favourites(state: State, favourites: list[str]) -> State:
  fav_indexes = [int(index) for index in favourites]
  favs = [state["post"].titles[index] for index in fav_indexes]
  return state.update(favourites=favs).append(favourites_draft=favs)


@action(reads=["favourites_draft"], writes=["final_result"])
def final_result(state: State) -> State:
    final_result = list(itertools.chain(*state["favourites_draft"]))
    return state.update(final_result=final_result)


application = (
  ApplicationBuilder()
  .with_actions(
    generate_titles.bind(llm_client=llm_client),
    select_favourites,
    final_result
  )
  .with_transitions(
    ("generate_titles", "select_favourites"),
    ("select_favourites", "final_result")
  )
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
while True:
  action, result, state = application.run(
    halt_before=["select_favourites"],
    halt_after=["final_result"],
    inputs=inputs,
  )

  if action.name == "select_favourites":
    c.print("Which ones do you like (if any)?", style="yellow")
    for index, title in enumerate(state["post"].titles):
      c.print(f"{index}: {title}")

    favourites = c.input("""
    [yellow]Enter numbers of ones you like. Empty to stop.\n[/]
    """.strip())
    inputs = {
      "favourites": ([] if favourites == "" else re.split(",[ ]*", favourites))
    }

  if action.name == "final_result":
    c.print("Here are all the ones you liked:")
    for item in state["final_result"]:
      c.print(item, style="green")
    break
