from typing import NamedTuple

class Movement():
	color: str = ''
	piece: str = ''
	destFile: str = ''
	destRank: str = ''
	disFile: str = None
	disRank: str = None
	take: bool = False
	castleLong: bool = False
	castleShort: bool = False
	crown: bool = False
	crownTo: str = None
	check: bool = False

	def __str__(self):
		# Override __str__ to print a readable string representation of the object
		return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])