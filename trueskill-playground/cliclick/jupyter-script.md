raycastSwitchApp:Arc jupyter
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter

```jupyter
from trueskill import Rating
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter

```jupyter
Rating()
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:1000||1

// Plot of base distribution
jupyter::notebook::command::b
jupyter::notebook::command::enter

```jupyter
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
from itertools import cycle

def visualise_distribution(**kwargs):
  fig = go.Figure()    
  min_x = min([r.mu-4*r.sigma for r in kwargs.values()])
  max_x = max([r.mu+4*r.sigma for r in kwargs.values()])
  x = np.arange(min_x, max_x, 0.001)

  colors = cycle(['black', 'blue', 'red', 'green', 'orange'])
  for key, value in kwargs.items():
      y = norm.pdf(x, value.mu, value.sigma)
      fig.add_trace(go.Scatter(x=x, y=y, mode='lines', fill='tozeroy', name=key, line_color=next(colors)))
  fig.show()
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:500||1

jupyter::notebook::command::b
jupyter::notebook::command::enter

```jupyter
visualise_distribution(base=Rating())
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:500||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
from trueskill import rate, rate_1vs1
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
p1 = Rating()
p2 = Rating()
rate_1vs1(p1, p2)
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

// Shortcut to compare players
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
p1, p2 = rate_1vs1(p1, p2)
p1, p2
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
p1, p2 = rate_1vs1(p1, p2, drawn=True)
p1, p2
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

// Compare them 10 times
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
for _ in range(0, 10):
    p1, p2 = rate_1vs1(p1, p2)
    print(p1, p2)
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

// Plot showing p1, p2, base
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
visualise_distribution(base=Rating(), p1=p1, p2=p2)
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||2
cliclick2:w:1000||1

// Multi comparison
jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
p1, p2, p3, p4, p5, p6 = [Rating() for _ in range(0,6)]
rate([[p1], [p2]])
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
rate([[p1, p2], [p3, p4]])
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
rate([[p1, p2], [p3, p4]], weights=[(1, 0.5), (1, 1)])
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1

jupyter::notebook::command::b
jupyter::notebook::command::enter
cliclick2:kp:page-down||1
```jupyter
rate([[p1, p2], [p3, p4], [p5], [p6]], ranks=[0, 2, 1, 3])
```
jupyter::notebook::edit::cmd+enter
cliclick2:w:100||1
cliclick2:kp:page-down||1
cliclick2:w:1000||1