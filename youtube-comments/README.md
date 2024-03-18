# Analysing and clustering YouTube comments

This is a Streamlit app that lets you analyse YouTube comments for a given video.
I also wrote [a blog post](https://www.markhneedham.com/blog/2024/02/27/clustering-youtube-comments-ollama-embeddings-nomic/) walking through how it works. 

## Pre requisites

You'll need to have a YouTube API key and have [Ollama](https://ollama.com/) installed locally.
The other dependenciese are in [pyproject.tom](pyproject.toml)

## Running the app

The code is in [app.py](app.py). You can run it like this:

```bash
poetry run streamlit run app.py
```

In this video, we'll learn how to analyse YouTube comments by using Ollama and the Nomic Embed embedding algorithm. We'll get help from Streamlit to make everything a bit more interactive, scikit-learn to detect clusters of comments, and plot.ly to avoid the app being walls of text!

#streamlit #nomic #embeddings #scikit-learn #ollama

Simon Willison's blog post/video - https://simonwillison.net/2023/Oct/23/embeddings/
Code - https://github.com/mneedham/LearnDataWithMark/blob/main/youtube-comments/README.md
Blog Post - https://www.markhneedham.com/blog/2024/02/27/clustering-youtube-comments-ollama-embeddings-nomic/
Ollama - https://ollama.ai/
Nomic AI - https://blog.nomic.ai/posts/nomic-embed-text-v1

Hosted Gorilla

```python
from openai import OpenAI

def get_gorilla_response(prompt="Call me an Uber ride type \"Plus\" in Berkeley at zipcode 94704 in 10 minutes", model="gorilla-openfunctions-v0", functions=[]):
    client = OpenAI(
        base_url = 'http://luigi.millennium.berkeley.edu:8000/v1',
        api_key='anything',
    )

    response = client.chat.completions.create(
        model="gorilla-openfunctions-v1",
        messages=[{"role": "user", "content": prompt}],
        functions=functions
    )

def get_gorilla_response(prompt="Call me an Uber ride type \"Plus\" in Berkeley at zipcode 94704 in 10 minutes", model="gorilla-openfunctions-v0", functions=[]):
    client = OpenAI(
        base_url = 'http://localhost:8080/v1',
        api_key='anything',
    )

    response = client.chat.completions.create(
        model="gorilla-openfunctions-v1",
        messages=[{"role": "user", "content": prompt}],
        functions=functions
    )
```

```python
# https://huggingface.co/TheBloke/gorilla-openfunctions-v1-GGUF/blob/main/gorilla-openfunctions-v1.Q5_K_M.gguf 

from llama_cpp import Llama

query = "Call me an Uber ride type \"Plus\" in Berkeley at zipcode 94704 in 10 minutes"
functions = [
    {
        "name": "Uber Carpool",
        "api_name": "uber.ride",
        "description": "Find suitable ride for customers given the location, type of ride, and the amount of time the customer is willing to wait as parameters",
        "parameters":  [{"name": "loc", "description": "location of the starting place of the uber ride"}, {"name":"type", "enum": ["plus", "comfort", "black"], "description": "types of uber ride user is ordering"}, {"name": "time", "description": "the amount of time in minutes the customer is willing to wait"}]
    }
]

llm = Llama(model_path="/Users/markhneedham/Downloads/gorilla-openfunctions-v1.Q5_K_M.gguf")
template = """
USER: <<question>> {prompt} <<function>> {functions_string}\nASSISTANT:"""
print(llm(template.replace('{prompt}', query).replace('{functions_string}', str(functions))))
```

I have a list of YouTube comments in a cluster and I need to come up with a short 1-5 sentence category to name them. What should it be? Only return the category name.

0:"Wow, this was a contentious one. Some folks are really eager to prove that function calling does call functions, or that I was just wrong in this video. But they just say it without providing any supporting information. <br><br>So if you think that I am wrong, and what I say in this video is not 100% factual, then please provide some sort of documentation or a tutorial or a video or anything that suggests that function calling in the base OpenAI API is not exactly how I described it. Don&#39;t just point to some other product as your example. If you have any evidence, I would be happy to do an update video. <br><br>This video talks specifically about the base OpenAI API. Otherwise, simply accept that function calling doesn&#39;t call functions and instead is all about formatting the output, which is incredibly valuable. It certainly improved at that when the json format option came available later on."
1:"Thanks Matt  - Appreciate the real world python code example.<br>Also, major props for tackling the confusion regarding the term &quot;function calling&quot;."
2:"Output formatting is really necessary feature. BUT Langchain library already does that. Langchain&#39;s StructuredOutputParser does the same. Why to use &quot;function calling&quot; feature ?"
3:"Do the llamas spit out the function calls?"
4:"I appreciate the video but it is click bait. I mean I had just decided to use response format JSON with my OpenAI prompt instead of tools/functions because the client kept talking about going open source and I knew that the function calling format wasn&#39;t actually supported by things like Ollama. But I clicked on your video due to your title thinking maybe I was missing something."
5:"I use phind function calling model"
6:"As someone who was new to the ai thing, I thought I was too dumb to be missing something in how function_calling does not actually mean the model calls function. Thanks for putting the fundamentals out loud."
7:"Hi and thanks for the vidéo ! I made a chat bot with ollama and some Mixtral persona, but I can&#39;t figure out how to format when it give some code example, maybe it&#39;s just iterating in the string chat output, sorry if it&#39;s a simple question. I just think maybe it would be easier with this function calling (youuuu). #&lt;3Ollama"
8:"It would be great for us not-yet-quite-so-experienced users of the various api&#39;s to understand why you think the OpenAI api is so painful to use with functions. It&#39;s more verbose but you probably need that to support more complex scenarios with multiple functions and multiple schemas. I mean, OpenAI does have a certain level of experience with these things, they don&#39;t add complexity for no reason."
9:"Don&#39;t care about the naming debate. But want to point out, that you don&#39;t pass in just a single function description, you can pass-in multiple. The functions take parameters and the model chooses what parameters to pass to which functions. Some parameters might be optional or have heuristics in their description explaining to the model when they are best used. The model does call a function by responding to you in a certain format, and you end-up calling the function, but the choices of parameters is up to the model. This is not just about formatting the responses and is a great way to enrich the capabilities of an agent with &quot;reasoning&quot; as the results of the function calls expand the context with new extra information. When I need the model to respond in a certain format - I just ask it to do that, without function calling. When I need the model to &quot;try&quot; to &quot;reason&quot; and call the right function with right parameters to expand context - I use function calling."
10:"I admit that until now I misunderstand function calling. Now I get it. I think &quot;format JSON&quot; is the better  name. Thumbs up, Matt!"
11:"Great video and explanation. Would be great to know how to get the missing parameters to add to the « function calling » when the user doesn’t put all of them. Does the llm manage it? Do the programmer manage it? Maybe an idea for a video ;)"
12:"Yeah, totally! OpenAI calling it &quot;function calling&quot; had me and my friends like, &quot;What the heck?&quot; It&#39;s a good marketing name but kinda ignorant! I don&#39;t like when marketers manipulate things like that. Another thing that still I can&#39;t get my head around of it is &quot;GPTs&quot;, again the marketing aspect is like you are beuilging your own GPT but reality is you just what OLLAMA nicely call it Modelfile! Anyway, beside asking the main model to returns JSON in the system message, one another thing is to use the main large model to get the initial response and then a smaller model which is fine-tuned extract structural info to generate the JSON. Mixing two models can do the job, but again it&#39;s not &quot;function calling,&quot;. Good content though - I just subscribed!"
13:"This is great I was so upseet when i actually found out how function calling would work , i was thinking you would go into pydantic and the amazing instructor library , perhaps that would be a great next video"
14:"“Function Calling” and JSON formatting is not the same in OpenAI API. The objective of “Function Calling” is not about formatting, but about letting the model figuring out <b>if</b> a function should be called and the model using the return value of the function to formulate a response. If just JSON formatting is wanted, then there is the optional argument /resonse_format/ that has to be set accordingly. - That’s why I am still curious if Llama (or any other model besides OpenAI’s GPTs) does support “Function Calling” - let it be another name and another kind of API."
15:"I’ve been using functional calling in a project where I ‘sync’ a chatbot conversation with dynamically loaded page content. The idea is to display relevant supporting content on screen during a chat conversation. I have it working perfectly with GPT4 (my current project makes over 20 function calls during a typical conversation) but is flaky when using GPT3.5 - but, for me, function calling has been a game changer in terms of what I can create as a web developer."
16:"Call it &quot;Function Capable Formatting&quot; (or at least I will) whether done by AI or human. The actual functions can be called via any CLI tooling... whether done by AI or human. I am just waiting for all of the Mamba backed GUI webchat apps called &quot;***GPT&quot; for the traffic hype, as if OPENai wasn&#39;t bad enough. There&#39;s always Apple to &quot;protect your privacy&quot;. LOL. <br><br>Thank you for the clarification. Now I can read the docs."
17:"I think function calling capable models are finetuned on function calling data, it&#39;s not just format: json. Anyway I have never expected the model to call the API, as the important thing is not the call but the data, also it works for your APIs so how can the model call them? Has anybody even been confused about that?"
18:"Thank you making this video that clarifies and demonstrates the nature of function calling using AI!  It seems to me that if someone was using OpenAI to do function calls, it would be because they want the functions censored by their systems.  Services like these could be exploted by developers creating websites that can trigger function calls, and may be a security risk to a user.  That may be the reason OpenAI moderates them?  However as your video makes clear, it is fairly simple for anyone to do something like an uncensored function call, so does it make sense to have a service for it at all?  Especially if it makes use of the already existing moderation tuned models.  <br><br>Fantastic tutorial and interesting commentary, I&#39;m looking forward to more!"
19:"Thanks for explaining function calls. I think a better name is functionformatting. It&#39;s nice to finally understand what the big deal is.  I played with your code to better understand it and found  that haversine seems to be bad. (pip install so is latests?)  But ignoring that, this jsons stuff seems to really taxing the system. 10 minutes for a response on a fairly good laptop, using gpu."
20:"Yes, I think function calling is very important. Maybe a video about fine tuning a model for function calling. ;-).  Great video. Thanks for taking time out to share your knowledge."
21:"Great video, thank you. While it’s nice to have the OpenAI API in case you have an app that requires it, I much prefer the native library. My language of choice is Python, but there’s no accounting for taste :)<br><br>I’d like to see you expand on Function Calling or Format JSON in two ways:<br>1. What Open Source LLMs handle that well? What fallbacks do you build in to ensure they respond in well-formatted JSON?<br>2. How do you combine Format JSON with RAG? Say in the use case where the RAG contains data that you want to query based on parameters through functions?"
22:"Matt - brilliant video as always, thank you. Experimenting here with &quot;function calling&quot; so this is of huge benefit. Appreciated."
23:"Agree function calling is a confusing name. But also think ollama falls a bit short here compared to openai. Defining a schema in text as part of the system prompt feels a little imprecise to me. llama.cpp has a feature called Grammars which allows precisely defining a schema in a way the LLM can reliably reproduce. If Ollama allowed a way of defining your own custom grammar as part of the API, or a passing a JSON schema which it converts to grammar, then I think it would be comparable to openai for function calling use cases."
24:"Thank you for sharing your insights on the &#39;function calling&#39; feature. I appreciate your perspective and the effort to demystify this concept for a wider audience. I&#39;d like to offer a clarification on the function calling feature as it pertains to AI models, particularly in the context of OpenAI&#39;s API, to enrich our understanding.<br><br>Function calling, as it is implemented by OpenAI, does indeed involve the model in the process of generating responses that incorporate the outcomes of predefined functions. The key distinction lies in how &#39;calling a function&#39; is conceptualized. Rather than formatting the output for external functions to be executed by the user&#39;s application, function calling enables the model to leverage internal or predefined functions during its response generation process. This means the model dynamically integrates the results of these functions into its output.<br><br>The feature is named &#39;function calling&#39; because it extends the model&#39;s capability to &#39;call&#39; upon these functions as part of forming its responses, not because the model executes functions in the traditional programming sense where code is run to perform operations. This naming might seem a bit abstract at first, but it accurately reflects the model&#39;s enhanced capability to internally reference functions to enrich its responses.<br><br>Understanding function calling in this light highlights its innovative approach to making model outputs more dynamic and contextually rich. It&#39;s not just about formatting data but about embedding the function&#39;s utility directly into the model&#39;s processing pipeline. This feature opens up new possibilities for integrating AI models with complex data processing and analysis tasks, directly within their response generation workflow.<br><br>I hope this explanation clarifies the intent and functionality behind the &#39;function calling&#39; feature. It&#39;s indeed a powerful tool that, when understood and utilized correctly, significantly broadens the scope of what AI models can achieve in their interactions."
25:"Function calling has great benefits. if an output of a function is required to complete the users prompt it will output the function name of it and wait till it get the response from the function which we have to provide from our API. Then it process that data and create an proper result. It&#39;s really easy to setup function calling in the playground tool"