from rich.console import Console

def view(thing):
  c = Console()
  if len(thing.split("\n")) < 15:
    c.print(thing)
  else:
    with c.pager():
      c.print(thing)

def read_file(file):
  with open(file, "r") as text_file:
    return text_file.read()