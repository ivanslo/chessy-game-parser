'''
The next lines are there to deal with python files importing each other inside `src`
'''
import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))



from src import parser
import pytest
from pytest_mock import mocker

class TestGameController:
	parser = ""
	lexer = ""


	def setup_class(self):
		self.parser = parser.ChessParser()
		self.lexer = parser.ChessLexer()

	
	def test_callback(self, mocker):
		callback = mocker.stub(name='callback fn')
		self.parser.setCallbackFunction( callback )
		self.parser.parse(self.lexer.tokenize('1. e4 e5 2. Nc3 B3a1 3. a3'))
		assert( 5 == callback.call_count )

	def test_callback_object(self, mocker):
		callback = mocker.stub(name='callback fn')
		self.parser.setCallbackFunction( callback )
		self.parser.parse(self.lexer.tokenize('1. e4'))
		assert( 1 == callback.call_count )
		


