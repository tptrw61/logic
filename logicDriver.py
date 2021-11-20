#!/usr/bin/python3
import pyinputplus as pyip
from enum import Enum
from logic import System, asciiSymbols, defaultSymbols, getSystem, standardSymbols, truthTableCompareSys, truthTableSys, unicodeSymbols, validSentence, validEvalSentence, \
	prettifySentence, evaluateSys, validitySys

class SettingsKeys(Enum):
	PRETTY_PRINT = 'Pretty Print'
class SettingsHelperKeys(Enum):
	PPRINT_USE_ASCII = 1

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
		SettingsKeys.PRETTY_PRINT.value: 2,
		SettingsHelperKeys.PPRINT_USE_ASCII.name: False
	}
	return settingsDict

def setup():
	settings = getDefaultSettings()
	settings[SettingsHelperKeys.PPRINT_USE_ASCII.name] = settings[SettingsKeys.PRETTY_PRINT.value] == 0
	if settings[SettingsKeys.PRETTY_PRINT.value] <= 1:
		asciiSymbols()
	elif settings[SettingsKeys.PRETTY_PRINT.value] == 2:
		defaultSymbols()
	elif settings[SettingsKeys.PRETTY_PRINT.value] == 3:
		standardSymbols()
	elif settings[SettingsKeys.PRETTY_PRINT.value] == 4:
		unicodeSymbols()

def main():
	setup()
	settingsDict = getDefaultSettings()
	options = ['Evaluate', 'Validity', 'Truth Table', 'Settings', 'Quit']
	while True:
		choice = pyip.inputMenu(options, 'Select an option:\n', numbered=True)
		print()
		if choice == 'Quit':
			break
		elif choice == 'Evaluate':
			evaluate(settingsDict)
		elif choice == 'Validity':
			validity(settingsDict)
		elif choice == 'Truth Table':
			truthTable(settingsDict)
		elif choice == 'Settings':
			settingsDict = settings(settingsDict)
	#print('done.')


def evaluate(settingsDict: dict):
	systems = [s.name for s in System if s.hasValuation]
	system = pyip.inputMenu(systems, 'Choose a system:\n', applyFunc=lambda s: s.upper(), postValidateApplyFunc=getSystem)
	sentence = pyip.inputCustom(validateEvalSentence(system), 'Enter a sentence: ', strip=True)
	v = evaluateSys(sentence, system)
	print(f"'{prettifySentence(sentence)}' evaluates to '{v.symbol}' in {system.name}")
	print()

def validity(settingsDict: dict):
	systems = [s.name for s in System]
	system = pyip.inputMenu(systems, 'Choose a system:\n', applyFunc=lambda s: s.upper(), postValidateApplyFunc=getSystem)
	sentence = pyip.inputCustom(validateSentence(system), 'Enter a sentence: ', strip=True)
	valid, counterExample = validitySys(sentence, system)
	if valid:
		print(f"'{prettifySentence(sentence)}' is valid in {system.name}")
	else:
		print(f"'{prettifySentence(sentence)}' is not valid in {system.name}")
		for letter, value in counterExample.items():
			print(f"\t'{letter}' = {value.symbol}")
	print()

def truthTable(settingsDict: dict):
	systems = [s.name for s in System if s.hasValuation]
	system = pyip.inputMenu(systems, 'Choose a system:\n', applyFunc=lambda s: s.upper(), postValidateApplyFunc=getSystem)
	sentenceCount = pyip.inputInt('Number of sentences (0-2): ', min=0, max=2)
	if sentenceCount == 0:
		print()
		return
	sentence1 = pyip.inputCustom(validateSentence(system), 'Enter a sentence: ', strip=True)
	if sentenceCount == 1:
		truthTableSys(sentence1, system, settingsDict[SettingsHelperKeys.PPRINT_USE_ASCII.name])
	elif sentenceCount == 2:
		sentence2 = pyip.inputCustom(validateSentence(system), 'Enter a sentence: ', strip=True)
		truthTableCompareSys(sentence1, sentence2, system, settingsDict[SettingsHelperKeys.PPRINT_USE_ASCII.name])
	print()

def settings(settingsDict: dict) -> dict:
	options = [s.value for s in SettingsKeys] + ['Debug', 'Back']
	defaultSettings = getDefaultSettings()
	while True:
		choice = pyip.inputMenu(options, 'Choose an option:\n', numbered=True)
		if choice == 'Back':
			break
		elif choice == 'Debug':
			debugSettings(settingsDict)
		elif choice == SettingsKeys.PRETTY_PRINT.value:
			print('Higher values means more unicode. Values range from 0 to 4')
			print('0 means that no unicode will be used')
			print('4 means that as much unicode as possible will be used')
			print(f'Default: {defaultSettings[choice]}')
			level = pyip.inputInt(f"Enter a value (current: {settingsDict[choice]}): ", min=0, max=4)
			settingsDict[choice] = level
			if level == 0:
				settingsDict[SettingsHelperKeys.PPRINT_USE_ASCII.name] = True
			else:
				settingsDict[SettingsHelperKeys.PPRINT_USE_ASCII.name] = False
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

def debugSettings(settingsDict: dict):
	options = ['Display Standard Settings', 'Display All Settings', 'Back']
	while True:
		choice = pyip.inputMenu(options, 'Choose an option:\n', numbered=True)
		if choice == 'Back':
			break
		elif choice == 'Display Standard Settings':
			print()
			print('Settings:')
			for k in SettingsKeys:
				print(f"\t{k.value}: {settingsDict[k.value]}")
			print()
		elif choice == 'Display All Settings':
			print()
			print('Settings:')
			for k, v in settingsDict.items():
				print(f"\t{k}: {v}")
			print()
	print()

if __name__ == '__main__':
	main()
