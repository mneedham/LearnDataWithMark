from gliner import GLiNER
import time
from rich.console import Console
from video_utils import colour_code_for

c = Console()

def fill_gaps(entities, text):
    chunks = []
    for prev_entity, next_entity in zip(entities[:-1], entities[1:]):
        chunks.append(prev_entity)
        start = prev_entity["end"]
        end = next_entity["start"]
        chunks.append({"start": start, "end": end, "text": text[start:end]})
    chunks.append(entities[-1])

    if len(entities) > 0:
        if entities[0]["start"] > 0:
            start = 0
            end = entities[0]["start"]
            start_chunk = {"start": start, "end": end, "text": text[start:end]}
            chunks.insert(0, start_chunk)
        if entities[-1]["end"] < len(text)-1:
            start = entities[-1]["end"]
            end = len(text)
            end_chunk = {"start": start, "end": end, "text": text[start:end]}
            chunks.append(end_chunk)
    return chunks

def render_labels(label_colour_codes):
    c = Console()
    c.print("Labels: ", end='')
    for label, colour in label_colour_codes.items():
        c.print(label, end='', style=f"bold white on {colour}")
        c.print("", end=' ')
    c.print()


def render_text(chunks, label_colour_codes):
    c = Console()
    for entity in chunks:
        colour = entity.get("label")
        if colour in label_colour_codes:
            style = f"bold white on {label_colour_codes[colour]}"
        else:
            style = "white on black"
        c.print(entity['text'], end='', style=style)


def annotate_text(text, labels, model):
    label_color_codes = {label: colour_code_for(label) for label in labels}
    render_labels(label_color_codes)

    start = time.time()
    entities = model.predict_entities(text, labels)
    end = time.time()
    render_text(fill_gaps(entities, text), label_color_codes)
    c.print(f"\nTime taken: {end-start:.2f} seconds")


# Load the model
model = GLiNER.from_pretrained("urchade/gliner_base")


# ClickHouse article
with open("data/atlas.txt", "r") as file:
    text = file.read()


labels = ["programming-language", "database", "date"]
annotate_text(text, labels, model)

# Tennis article
with open("data/tennis.txt", "r") as file:
    text = file.read()

labels = ['person', 'location', 'event', 'score']
annotate_text(text, labels, model)

# Stability AI article
with open("data/stability.txt", "r") as file:
    text = file.read()

labels = ['organization', 'person', 'technology']
annotate_text(text, labels, model)
