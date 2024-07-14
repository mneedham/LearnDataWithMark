import uuid
import duckdb
from langchain_text_splitters import RecursiveCharacterTextSplitter

file = "data/ep68.txt"
with open(file, 'r') as reader:
    texts = reader.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=0,
    length_function=len,
    is_separator_regex=False,
)

documents = text_splitter.create_documents(texts)
print(len(documents))   

con = duckdb.connect("podcasts.duckdb")
con.sql("""CREATE TABLE podcast_transcript (
id STRING,
episode INTEGER,
paragraphNumber INTEGER,
text STRING
)""")

for index, document in enumerate(documents):
  con.execute(
    "INSERT INTO podcast_transcript VALUES (?, ?, ?, ?)", 
    [str(uuid.uuid4()), 68, index, document.page_content]
  )

con.sql("INSTALL fts")
con.sql("LOAD fts")
con.sql("""
PRAGMA create_fts_index(
    'podcast_transcript', 'id', 'text', overwrite=1
);
""")