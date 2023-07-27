raycastSwitchApp:Arc jupyter
cliclick2:w:1000||1

// Navigate into position
cliclick::multiCommand::kp:arrow-up||3
cliclick2:w:500||1
jupyter::notebook::command::c
cliclick::multiCommand::kp:arrow-down||3
cliclick2:w:500||1
cliclick2:kp:page-down||1
jupyter::notebook::command::v
cliclick2:w:500||1

// Into the codes
jupyter::notebook::command::enter
cliclick::multiCommand::kp:arrow-down||19
cliclick::multiCommand::kp:arrow-up||7
cliclick::multiCommand::kd:cmd||kp:arrow-right||ku:cmd||ku:fn||1

```oneLine
,
```

```jupyter
        functions=[{"name": "dummy_fn_set_sentiment", "parameters": {
          "type": "object",
          "properties": {
            "sentiments": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "sentiment": {"type": "string", "description": "Sentiment of the review"},
                  "sentiment_score": {"type": "integer","description": "Score between 1-100 of the sentiment"}
                }
              }
            }
          }
        }}],
```
cliclick::multiCommand::kp:arrow-down||3
cliclick::multiCommand::kd:cmd||kp:arrow-right||ku:cmd||ku:fn||1
cliclick::multiCommand::kd:alt||kp:delete||ku:alt||ku:fn||1


```singleLineNoEnter
function_call.arguments
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
sentiments = analyse_reviews(reviews)
sentiments
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:7000||1
cliclick2:kp:page-down||1
cliclick2:w:3000||1

jupyter::notebook::edit::cmd+enter
cliclick2:w:7000||1
cliclick2:kp:page-down||1
cliclick2:w:3000||1

jupyter::notebook::edit::cmd+enter
cliclick2:w:7000||1
cliclick2:kp:page-down||1
cliclick2:w:3000||1

// Join DataFrames 
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
sentiment_df = pd.DataFrame(sentiments["sentiments"])
result = pd.concat([reviews_df, sentiment_df], axis=1)
pd.set_option('max_colwidth', 100)
result
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:500||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1