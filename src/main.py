import click
import GameController


@click.command()
@click.option('--pgnGame', required=True, help='Game to be parsed (PGN Format)')
@click.option('--outputFile', required=True, help='File to be created')
def command(**kwargs):
    pgnGame = ""
    with open(kwargs['pgngame'], 'r') as inputGame:
        lines = inputGame.readlines()
        pgnGame = "".join(lines)

    processedGame = GameController.processGame(pgnGame)
    with open(kwargs['outputfile'], 'w') as f:
        f.write(processedGame)



if __name__ == "__main__":
    # parser()
    command()