from rich.console import Console


def view(item):
  c = Console()
  with c.pager(styles=True):
    c.print(item)
