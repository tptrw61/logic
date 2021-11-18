#!/usr/bin/python3
import sys
from argh import arg, dispatch_command
from logic import System, asciiSymbols, defaultSymbols, entailmentSys, unicodeSymbols, standardSymbols, prettifySentence

def getSystem(system: str) -> System:
    for syst in System:
        if system == syst.name:
            return syst

@arg('premise', nargs='+', type=str)
@arg('sentence', type=str)
@arg('-s', '--system', choices=['PL', 'K', 'L', 'LP'])
@arg('-a', '--ascii', action='count', help='the more acsii flags, the less unicode (default=4)')
def main(system: str='PL', quiet=False, **kwargs):
    premises = ','.join(kwargs['premise']).replace(' ', '')
    sentence = kwargs['sentence'].replace(' ', '')
    isValid, counterExample = entailmentSys(premises, sentence, getSystem(system))
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
        print(f"'{prettifySentence(premises.replace(',', ', '))}' entails '{prettifySentence(sentence)}' in {system}")
    else:
        print(f"'{prettifySentence(premises.replace(',', ', '))}' does not entail '{prettifySentence(sentence)}' in {system}")
        for letter, value in counterExample.items():
            print(f"\t'{letter}' = {value.symbol}")

if __name__ == '__main__':
    dispatch_command(main)
