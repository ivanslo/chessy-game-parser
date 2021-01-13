import click
import PGNFile


@click.command()
@click.option('--pgnFile', required=True, help='File to be splitted (PGN Format)')
def command(**kwargs):
	inputFilename = kwargs['pgnfile']

	# very trivial way to check for the extension
	if inputFilename[-4:] != ".pgn":
		print("The input file should be .pgn")
		return

	getGameLines(inputFilename)
	# getChunks(inputFilename)


def getGameLines(pgnFileName: str):
	with open(pgnFileName, 'r') as ig:
		lines = ig.readlines()
		boundaries = PGNFile.getGameBoundaryLines(lines)

		chunks = PGNFile.groupBoundaries(boundaries, 200)
		
		for (f,t) in chunks:
			print('{0} {1}'.format(f,t))

def getChunks(pgnFileName: str):
	with open(pgnFileName, 'r') as inputGame:
		lines = inputGame.readlines()
		boundaries = PGNFile.getGameBoundaryLines(lines)
		chunks = PGNFile.groupBoundaries(boundaries, 200)
		for i, (f,t) in enumerate(chunks):
			outputFileName = "%s_chunked_%d.pgn" % (pgnFileName[:-4], i)
			with open(outputFileName, 'w') as outputFile:
				outputFile.writelines(lines[f:t])


if __name__ == "__main__":
	command()
