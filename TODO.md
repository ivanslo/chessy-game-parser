- [ DONE ] investigate Struct/types in Python
- [ DONE ] narrow down the components Movement should have - what about castle?
- [ DONE ] Parser creates a Movement well done
- [ DONE ] GameController gets the callback from parser and calls makeMove in Board

- [ PROGRESS ]Board starts with [identity]; after receiving the movement, it computes its next position
	- [x] Pawn
	- [x] Bishop
	- [x] Knight
	- [ ] Rook
	- [ ] Queen
	- [ ] King

- [ ] Add TESTS!
- find a fancy way to write the functions.. with decorators and so on. For example, moveKnight/moveBishop/movePawn could be done without having a big if-else I guess
---

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
