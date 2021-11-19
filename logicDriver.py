#!/usr/bin/python3
import pyinputplus as pyip
from logic import System, asciiSymbols, defaultSymbols, getSystem, standardSymbols, unicodeSymbols, validSentence, validEvalSentence, \
	prettifySentence, evaluateSys, validitySys

def getSystemCaseInsensitive(system: str) -> System:
	return getSystem(system.upper())

def toUpper(s: str) -> str:
	return s.upper()

def validateEvalSentence(system: System):
	def func(text: str):
		if not validEvalSentence(text, system):
			raise Exception(f"'{prettifySentence(text)}' is not a valid sentence in {system.name}")
	return func
def validateSentence(system: System):
	def func(text: str):
		if not validSentence(text, system):
			raise Exception(f"'{prettifySentence(text)}' is not a valid sentence in {system.name}")
	return func

def getDefaultSettings() -> dict:
	settingsDict = {
		'Pretty Print': 2
	}
	return settingsDict

def setup():
	settings = getDefaultSettings()
	if settings['Pretty Print'] <= 1:
		asciiSymbols()
	elif settings['Pretty Print'] == 2:
		defaultSymbols()
	elif settings['Pretty Print'] == 3:
		standardSymbols()
	elif settings['Pretty Print'] == 4:
		unicodeSymbols()

def main():
	setup()
	settingsDict = getDefaultSettings()
	options = ['Evaluate', 'Validity', 'Settings', 'Quit']
	while True:
		choice = pyip.inputMenu(options, 'Select an option:\n', numbered=True)
		print()
		if choice == 'Quit':
			break
		elif choice == 'Evaluate':
			evaluate(settingsDict)
		elif choice == 'Validity':
			validity(settingsDict)
		elif choice == 'Settings':
			settingsDict = settings(settingsDict)
	#print('done.')


def evaluate(settingsDict: dict):
	systems = [s.name for s in System if s.hasValuation]
	system = pyip.inputMenu(systems, 'Choose a system:\n', applyFunc=toUpper, postValidateApplyFunc=getSystem)
	sentence = pyip.inputCustom(validateEvalSentence(system), 'Enter a sentence: ', strip=True)
	v = evaluateSys(sentence, system)
	print(f"'{prettifySentence(sentence)}' evaluates to '{v.symbol}' in {system.name}")
	print()

def validity(settingsDict: dict):
	systems = [s.name for s in System]
	system = pyip.inputMenu(systems, 'Choose a system:\n', applyFunc=toUpper, postValidateApplyFunc=getSystem)
	sentence = pyip.inputCustom(validateSentence(system), 'Enter a sentence: ', strip=True)
	valid, counterExample = validitySys(sentence, system)
	if valid:
		print(f"'{prettifySentence(sentence)}' is valid in {system.name}")
	else:
		print(f"'{prettifySentence(sentence)}' is not valid in {system.name}")
		for letter, value in counterExample.items():
			print(f"\t'{letter}' = {value.symbol}")
	print()

def settings(settingsDict: dict) -> dict:
	options = list(settingsDict.keys()) + ['Back']
	defaultSettings = getDefaultSettings()
	while True:
		choice = pyip.inputMenu(options, 'Choose an option:\n', numbered=True)
		if choice == 'Back':
			break
		elif choice == 'Pretty Print':
			print('Higher values means more unicode. Values range from 0 to 4')
			print('0 means that no unicode will be used')
			print('4 means that as much unicode as possible will be used')
			print(f'Default: {defaultSettings[choice]}')
			level = pyip.inputInt(f"Enter a value (current: {settingsDict[choice]}): ", min=0, max=4)
			settingsDict[choice] = level
			if level <= 1:
				asciiSymbols()
			elif level == 2:
				defaultSymbols()
			elif level == 3:
				standardSymbols()
			elif level == 4:
				unicodeSymbols()
	print()
	return settingsDict

if __name__ == '__main__':
	main()
