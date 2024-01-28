from IPython.core.magic import register_line_magic, register_cell_magic, register_line_cell_magic
import time
from rich.console import Console

console = Console()

@register_line_cell_magic
def timecell(line, cell=None):
    "Magic that can time the execution of a single line or a cell."
    start_time = time.time()
    
    if cell is None:
        # Line magic mode
        get_ipython().run_line_magic('time', line)
    else:
        # Cell magic mode
        get_ipython().run_cell(cell)
    
    end_time = time.time()
    console.print(f"\nExecution time: {end_time - start_time:.2f} seconds", style="yellow")

def load_ipython_extension(ipython):
    """This function is called when the extension is loaded."""
    # No need to register it twice; the @register_line_cell_magic does it for both.