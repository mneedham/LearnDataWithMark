from markdown_it import MarkdownIt
from rich.console import Console

def parse_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    md = MarkdownIt()
    tokens = md.parse(content)
    result = {}
    
    open_headings = {}

    current_heading = None
    current_heading_tag = None
    current_content = []

    first_heading = next(
        idx 
        for idx, t in enumerate(tokens) 
        if t.type == "heading_open" and t.tag == "h1"
    )

    for token in tokens[first_heading:]:
        if token.type == 'heading_open':
            if current_heading and current_content:
                result[current_heading] = '\n'.join(current_content).strip()
            current_heading = None
            current_heading_tag = token.tag
            current_content = []
        elif token.type == 'inline' and current_heading is None:
            if current_heading_tag == "h1":
                open_headings = {}
                current_heading = token.content
                open_headings[current_heading_tag] = current_heading
            else:
                sorted_open_headings = sorted(open_headings.items(), key=lambda x: x[0])
                prev_headings = [
                    (k,v) 
                    for k,v in sorted_open_headings 
                    if k.replace("h", "") < current_heading_tag.replace("h", "")
                ]
                prev_headings = tuple([v for _,v in prev_headings])
                current_heading = prev_headings + (token.content,)
                open_headings[current_heading_tag] = token.content
        elif token.type == 'paragraph_open':
            continue
        elif token.type == 'inline' and current_heading:
            current_content.append(token.content)

    if current_heading and current_content:
        result[current_heading] = '\n'.join(current_content).strip()

    return result


def view(item):
  c = Console()
  with c.pager(styles=True):
    c.print(item)    


def print_stream(response):
  c = Console()
  for chunk in response:
    c.print(chunk, end="")