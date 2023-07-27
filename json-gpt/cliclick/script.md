raycastSwitchApp:Arc jupyter
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter

```jupyter
import openai
import json
import pandas as pd
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
```jupyter
reviews_df = pd.read_csv("reviews.csv")
reviews = reviews_df['review'].tolist()
reviews
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:500||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
def analyse_reviews(user_input):
    prompt = f"""
    {user_input}
    Analyse the sentiment of the reviews above and return a JSON array as the result.
Provide sentiment on a scale of 1-100?
The JSON must have these fields: sentiment, sentiment_score.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful review analysis tool."},
            {"role": "user", "content": prompt},
        ]
    )

    try:
        generated_text = completion.choices[0].message.content
        return json.loads(generated_text)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:500||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

// Run once
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
analyse_reviews(reviews)
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:7000||1
cliclick2:kp:page-down||1
cliclick2:w:3000||1

// Run again
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
analyse_reviews(reviews)
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:7000||1
cliclick2:kp:page-down||1
cliclick2:w:3000||1

// And again
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
analyse_reviews(reviews)
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:7000||1
cliclick2:kp:page-down||1
cliclick2:w:3000||1
