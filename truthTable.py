#!/usr/bin/python3
from argh import arg
from argh.dispatching import dispatch_command
from logic import System, asciiSymbols, defaultSymbols, truthTableSys, truthTableCompareSys, standardSymbols, prettifySentence, unicodeSymbols

def getSystem(system: str) -> System:
	for syst in System:
		if system == syst.name:
			return syst

@arg('-s', '--system', choices=['PL', 'K', 'L'])
@arg('sentence2', nargs='?', default=None, type=str)
@arg('-a', '--ascii', action='count', help='the more acsii flags, the less unicode (default=4)')
def main(sentence: str, system: str='PL', **kwargs):
	if kwargs['ascii'] == None:
		kwargs['ascii'] = 4
	
	if kwargs['ascii'] == 1:
		unicodeSymbols()
	elif kwargs['ascii'] == 2:
		standardSymbols()
	elif kwargs['ascii'] == 3:
		defaultSymbols()
	elif kwargs['ascii'] >= 4:
		asciiSymbols()
	useAscii = False
	if kwargs['ascii'] >= 5:
		useAscii = True

	if kwargs.get('sentence2', None) == None:
		truthTableSys(sentence, getSystem(system), useAscii)
	else:
		truthTableCompareSys(sentence, kwargs['sentence2'], getSystem(system), useAscii)

if __name__ == '__main__':
	dispatch_command(main)
