Tips:

- unalias python

Resources in Browser:

- sly doc: https://sly.readthedocs.io/en/latest/sly.html#writing-a-parser
- youtube talk: https://www.youtube.com/watch?v=zJ9z6Ge-vXs

Interpreter Commands: (test on the flight)

```
from src import parser

lexer = parser.ChessLexer()
pr = parser.ChessParser()

pr.parse(lexer.tokenize(" "))
```
