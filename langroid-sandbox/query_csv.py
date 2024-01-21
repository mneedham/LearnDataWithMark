import langroid as lr
import langroid.language_models as lm
from langroid.utils.configuration import set_global, Settings
import pandas as pd
from langroid.agent.special import TableChatAgent, TableChatAgentConfig


# No exponential numbers
pd.set_option('display.float_format', lambda x: f'{x:.3f}')

# Hide annoying Redis message!
set_global(Settings(cache_type="fakeredis"))

# Configure Mixtral LLM

llm_cfg = lm.OpenAIGPTConfig(
    chat_model="litellm/ollama/mixtral",
    chat_context_length=4096,
)
llm = lm.OpenAIGPT(llm_cfg)


# Warm up

response = llm.chat("What is pandas in up to 3 bullet points?")

# Load CSV file

dataset="data/world_population_data.csv"
df = pd.read_csv(dataset)
df.columns
df.head().T

# Configure agent


agent = TableChatAgent(
    config=TableChatAgentConfig(data=dataset,llm=llm_cfg)
)

task = lr.Task(agent, name = "DataAssistant", default_human_response="")


# Top population
message = "What are the top 5 countries in terms of population?"
result = task.run(message, turns=2)

(df
  .sort_values(by=["2023 population"], ascending=False)
  [["country", "2023 population"]]
  .head()
)


# Biggest population increase

message = "Who had the biggest absolute population increase from 1970 to 2023?"
result = task.run(message, turns=2)

df["absoluteChange"] = df["2023 population"] - df["1970 population"]
(df
  .sort_values(by=["absoluteChange"], ascending=False)
  [["country", "2023 population", "1970 population", "absoluteChange"]]
  .head()
)

# What's the average, min, and max area for each continent?


message = "What's the average, min, and max area for each continent?"
result = task.run(message, turns=2)

(df.groupby(["continent"])["area (km²)"]
    .agg(["min", "mean", "max"])
)