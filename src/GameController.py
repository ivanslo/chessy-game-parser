import parser as pr
import sys
import Board


__board = Board.Board()
def printSomething(aa):
	print("")
	print("Movement: ", aa)
	__board.makeMovement(aa)
	__board.printBoard()
	
	
def main():
	print("----------------------")

	lexer  = pr.ChessLexer()
	parser = pr.ChessParser()

	parser.setCallbackFunction( printSomething )

	# parser.parse(lexer.tokenize('1. e4 B3a1 2.Nf3 e6+ 3. bxa3 O-O 4. O-O-O K3e4 5. a8=Q'))
	# parser.parse(lexer.tokenize(sys.stdin.read()))

	# normal pawn
	# parser.parse(lexer.tokenize("1. e4 e5 2. d4 exd4"))

	# am passand
	# parser.parse(lexer.tokenize("1. e4 a6 2. e5 f5 3. exf6 "))

	# impossible
	# parser.parse(lexer.tokenize("1. e5 e4"))

	# normal Bishop
	# parser.parse(lexer.tokenize("1. e4 e5 2. Bc4 d6 3. d3 Bf5"))

	# normal Knight
	# parser.parse(lexer.tokenize("1. Nf3 Nh6"))
	# ambiguous Knight
	parser.parse(lexer.tokenize("1. Nf3 Nf6 2. Nc3 Nc6 3. Nd4 Nd5 5. Ncb5 Ndb4 6. Nxc6 dxc6 7. Nd4"))
main()
