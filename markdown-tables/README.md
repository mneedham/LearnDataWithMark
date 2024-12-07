# Can LLMs understand markdown tables?

Converting Novak Djokovic's career statistics page to a markdown file:

```bash
uv run --with docling --with numpy==1.26.4 \
docling \
https://en.wikipedia.org/wiki/Novak_Djokovic_career_statistics
```

View the markdown file:

```bash
cat Novak_Djokovic_career_statistics.md
```

Launch iPython:

```bash
uv run \
--with markdown-it-py --with openai \
--with ipython --with llm \
ipython
```

Parse the markdown file:

```python
from utils import parse_markdown, view

novak = parse_markdown('Novak_Djokovic_career_statistics.md')
```

Extract one section:

```python
finals = novak[
    (
  'Novak Djokovic career statistics', 
  'Grand Slam tournaments', 
  'Grand Slam tournament finals: 37 (24 titles, 13 runner-ups)'
)
]
```

Initialise LLM:

```python
from utils import print_stream
import llm
model = llm.get_model("gpt-4o")
```

Initialise conversation:

```python
conversation = model.conversation()
response = conversation.prompt(
  prompt=finals,
  system="""I'm going to provide you with a markdown table and
  then I'll ask questions about it. Sound good?"""
)
```

What was his first title?

```python
response = conversation.prompt("""
What was the first title win?
""")
print_stream(response)
```

How did he do on hard courts?

```python
response = conversation.prompt("""
And how did he do on hard courts?
Think through it step by step.
""")
print_stream(response)
```

Extract the top level singles title:

```python
singles = novak[
(
  'Novak Djokovic career statistics',
  'Performance timelines',
  'Singles'
)
]
```

Initialise new conversation to use new section:

```python
conversation = model.conversation()
response = conversation.prompt(
  prompt=singles,
  system="""I'm going to provide you with a markdown table and
  then I'll ask questions about it. Sound good?"""
)
```

What was his best year?

```python
response = conversation.prompt("""
What was his best year?
Think through it step by step.
""")
print_stream(response)
```

Top 3 ranking

```python
response = conversation.prompt("""
What years did he finish ranked in the top 3?
Think through it step by step.
""")
print_stream(response)
```