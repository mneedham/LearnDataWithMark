import base64
from io import BytesIO
from PIL import Image
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os

# def display_pil_image(pil_image, scale=1.0):
#     if scale != 1.0:
#         width, height = pil_image.size
#         new_width = int(width * scale)
#         new_height = int(height * scale)
#         pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)

#     buffer = BytesIO()
#     pil_image.save(buffer, format="PNG")
#     image_bytes = buffer.getvalue()

#     encoded_string = base64.b64encode(image_bytes).decode()

#     print(f'\x1b]1337;File=inline=1:{encoded_string}\a')

def display_image(pil_image, scale=1.0, max_width=None, max_height=1200):
  print(displayable_image(pil_image, scale, max_width, max_height))

def resize_image(pil_image, scale=1.0, max_width=None, max_height=1200):
    if scale != 1.0 or max_width or max_height:
        width, height = pil_image.size
        
        if scale != 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
        else:
            new_width, new_height = width, height

        if max_width and new_width > max_width:
            new_width = max_width
            new_height = int(height * (max_width / width))

        if max_height and new_height > max_height:
            new_height = max_height
            new_width = int(width * (max_height / height))

        pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
    return pil_image


def displayable_image(pil_image, scale=1.0, max_width=None, max_height=1200):
    pil_image = resize_image(pil_image, scale, max_width, max_height)

    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    encoded_string = base64.b64encode(image_bytes).decode()

    return f'\x1b]1337;File=inline=1:{encoded_string}\a'


def view(item):
  c = Console()
  with c.pager(styles=True):
    c.print(item)


def as_table(rows):
  table = Table(show_header=True)
  table.add_column("Path")
  table.add_column("Image")

  for row in rows:
    table.add_row(
      row.image_uri, 
      imgcat(row.image)
    )
  return table



# Usage examples:
# display_pil_image(rs[0].image)  # Original size
# display_pil_image(rs[0].image, scale=0.5)  # Half size
# display_pil_image(rs[0].image, max_width=300)  # Limit width to 300 pixels
# display_pil_image(rs[0].image, max_height=200)  # Limit height to 200 pixels