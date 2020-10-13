import re

class GameMetadata:
    metadata_regex = r'\[(\w+)\s*"(.*)"\]'

    def __init__(self):
        self.gameInfo = []
        self.metadata_matcher = re.compile(self.metadata_regex)
        self.gameInfoDict = {}
    
    def add(self, metadata: str):
        m = self.metadata_matcher.match(metadata)
        self.gameInfoDict[m.group(1)] = m.group(2)
        self.gameInfo.append(metadata)


    # apparently there are a seven mandatory fields for PGN files: https://en.wikipedia.org/wiki/Portable_Game_Notation
    # the resulting id is made out with the VALUE of those fields (if present)
    _mandatoryFields = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]

    def getId(self):
        idmakers = []
        for key in self.gameInfoDict.keys():
            if key in self._mandatoryFields:
                idmakers.append(self.gameInfoDict[key])
        
        id = "_".join(idmakers)
        id = id.replace(" ", "")
        id = id.replace(",", "")
        id = id.replace(".", "")
        id = id.replace("/", "")
        id = id.replace("-", "")
        return id