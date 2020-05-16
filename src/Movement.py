from typing import NamedTuple


class Movement():
	# mandatory
	color: str = ''
	piece: str = ''
	destFile: str = ''
	destRank: str = ''
	# optional
	disFile: str = None
	disRank: str = None
	take: bool = False
	castleLong: bool = False
	castleShort: bool = False
	crown: bool = False
	crownTo: str = None
	check: bool = False

	def __str__(self):
		#return ('Movement {piece} {destFile} {destRank} ({disFile} {disRank}) x:{take} ...').format(self.__dict__)
		# Override to print a readable string presentation of your object
		# below is a dynamic way of doing this without explicity constructing the string manually
		return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])
