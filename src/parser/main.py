import click
import GameController


@click.command()
@click.option('--pgnFile', required=True, help='File to be parsed (PGN Format)')
@click.option('--partialFrom', required=False, help='Specify lower line limit', type=click.INT)
@click.option('--partialTo', required=False, help='Specify upper line limit', type=click.INT)
def command(**kwargs):
	inputFilename = kwargs['pgnfile']

	# very trivial way to check for the extension
	if inputFilename[-4:] != ".pgn":
		print("The input file should be .pgn")
		return

	inputPartialFrom = kwargs.get('partialfrom', None)
	inputPartialTo = kwargs.get('partialto', None)

	if not ((inputPartialFrom and inputPartialTo) or (not inputPartialFrom and not inputPartialTo)):
		print("Either both or none should be specified: --partialFrom , --partialTo")
		return

	if inputPartialFrom and inputPartialTo:
		GameController.processPGNFilePartial(inputFilename, inputPartialFrom, inputPartialTo)
	else:
		GameController.processPGNFile(inputFilename)

if __name__ == "__main__":
	command()
