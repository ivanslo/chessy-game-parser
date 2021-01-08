import parser as pr
import sys

def getGameBoundaryLines( filelines: [str]) -> [(int, int)]:
    # the algorithm can be described as:
    #   begin: with a [
    #       continue until we stop seeing [  (game)
    #   ends with the next [ or EOF

    chunks = []

    i = 0
    beginning = i
    while i < len(filelines):
        if filelines[i].startswith('['):
            beginning = i
            while i < len(filelines) and filelines[i].startswith('['):
                # we're in intro
                i += 1
            while i < len(filelines) and not filelines[i].startswith('['):
                i += 1
            chunks.append((beginning, i))
        else:
            i += 1

    return chunks


def groupBoundaries(boundaryLines: [(int, int)], groupSize: int) -> [(int, int)]:
    newBoundaries = []
    start = 0
    while start < len(boundaryLines):
        end = start + groupSize
        subgroup = boundaryLines[start:end]

        f = subgroup[0][0]
        t = subgroup[len(subgroup)-1][1]
        newBoundaries.append((f,t))
        start = end
    return newBoundaries