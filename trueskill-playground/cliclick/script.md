raycastSwitchApp:iTerm 2 python
selectWindow:2
clearScreen
cliclick2:w:1000||1

```python
from trueskill import Rating, rate, rate_1vs1
```
cliclick2:w:1000||1

```python
alcaraz, djokovic, rune, sinner = [Rating() for _ in range(4)]

```
cliclick2:w:1000||1

```python
alcaraz
```
cliclick2:w:1000||1
clearScreen

```python
rate_1vs1(alcaraz, rune)
```
cliclick2:w:1000||1

```python
rate_1vs1(alcaraz, rune)
```
cliclick2:w:1000||1

```python
alcaraz, rune = rate_1vs1(alcaraz, rune)
```