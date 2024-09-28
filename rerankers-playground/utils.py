from rich.console import Console
from rich.table import Table


def view(item):
  c = Console()
  with c.pager(styles=True):
    c.print(item)