import click
import GameController


@click.command()
@click.option('--pgnFile', required=True, help='File to be parsed (PGN Format)')
def command(**kwargs):
	inputFilename = kwargs['pgnfile']

	# very trivial way to check for the extension
	if inputFilename[-4:] != ".pgn":
		print("The input file should be .pgn")
		return

	GameController.processPGNFile(inputFilename)

if __name__ == "__main__":
	command()
