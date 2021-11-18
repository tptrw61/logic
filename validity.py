#!/usr/bin/python3
import sys
from argh import arg, dispatch_command
from logic import System, asciiSymbols, defaultSymbols, unicodeSymbols, validitySys, standardSymbols, prettifySentence

def getSystem(system: str) -> System:
    for syst in System:
        if system == syst.name:
            return syst

@arg('-s', '--system', choices=['PL', 'K', 'L', 'LP'])
@arg('-a', '--ascii', action='count', help='the more acsii flags, the less unicode (default=4)')
def main(sentence: str, system: str='PL', quiet=False, **kwargs):
    isValid, counterExample = validitySys(sentence, getSystem(system))
    if quiet:
        if isValid:
            sys.exit(0)
        else:
            sys.exit(1)

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
    
    if isValid:
        print(f"'{prettifySentence(sentence)}' is valid in {system}")
    else:
        print(f"'{prettifySentence(sentence)}' is not valid in {system}")
        for letter, value in counterExample.items():
            print(f"\t'{letter}' = {value.symbol}")

if __name__ == '__main__':
    dispatch_command(main)
