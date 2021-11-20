from enum import Enum
from typing import Tuple

class Value(Enum):
	FALSE = 0
	HASH = .5
	TRUE = 1
	
	@property
	def symbol(self) -> str:
		lookup = {0: '0', .5: '#', 1: '1'}
		return lookup[self.value]

class System(Enum):
	PL = 1
	K = 2
	L = 3
	LP = 4

	@property
	def hasValuation(self) -> bool:
		return self != System.LP

def getValue(v: str) -> Value:
	for val in Value:
		if v == val.symbol:
			return val
def getSystem(system: str) -> System:
	for syst in System:
		if system == syst.name:
			return syst

def land(a: Value, b: Value) -> Value:
	return Value(min(a.value, b.value))
land.unicodeSymbol = '\u2227'
land.asciiSymbol = '^'
land.symbol = land.asciiSymbol #bc windows

def lor(a:Value, b: Value) -> Value:
	return Value(max(a.value, b.value))
lor.unicodeSymbol = '\u2228'
lor.asciiSymbol = 'v'
lor.symbol = lor.asciiSymbol #bc windows

def lneg(a: Value) -> Value:
	return Value(1 - a.value)
lneg.unicodeSymbol = '~'
lneg.asciiSymbol = '~'
lneg.symbol = lneg.unicodeSymbol

def limpliesK(a: Value, b: Value) -> Value:
	return lor(lneg(a), b) #this holds true in K
limpliesK.unicodeSymbol = '\u2192' #right arrow
limpliesK.asciiSymbol = '->'
limpliesK.symbol = limpliesK.unicodeSymbol

def limpliesL(a: Value, b: Value) -> Value:
	if a == b:
		return Value.TRUE
	else:
		return limpliesK(a, b)
limpliesL.unicodeSymbol = '\u2192'
limpliesL.asciiSymbol = '->'
limpliesL.symbol = limpliesL.unicodeSymbol

def liffK(a: Value, b: Value) -> Value:
	return land(limpliesK(a, b), limpliesK(b, a))
liffK.unicodeSymbol = '\u2194'
liffK.asciiSymbol = '<->'
liffK.symbol = liffK.unicodeSymbol

def liffL(a: Value, b: Value) -> Value:
	return land(limpliesL(a, b), limpliesL(b, a))
liffL.unicodeSymbol = '\u2194'
liffL.asciiSymbol = '<->'
liffL.symbol = liffL.unicodeSymbol

def ldef(a: Value) -> Value:
	if a == Value.TRUE:
		return Value.TRUE
	else:
		return Value.FALSE
ldef.unicodeSymbol = '\u25b3'
ldef.asciiSymbol = '!'
ldef.symbol = ldef.asciiSymbol

def leq(a: Value, b: Value) -> Value:
	#(!(~P^~Q)v((~!P^~!~P)^(~!Q^~!~Q)))v!(P^Q)
	p0 = ldef(land(lneg(a), lneg(b)))
	ph1 = land(lneg(ldef(a)), lneg(ldef(lneg(a))))
	ph2 = land(lneg(ldef(b)), lneg(ldef(lneg(b))))
	ph = land(ph1, ph2)
	p1 = ldef(land(a, b))
	return lor(lor(p0, ph), p1)
	if a == b:
		return Value.TRUE
	return Value.FALSE
leq.unicodeSymbol = '='
leq.asciiSymbol = '='
leq.symbol = leq.asciiSymbol

functions = [lneg, land, lor, limpliesK, limpliesL, liffK, liffL, ldef, leq]
staticBinaryFunctions = [lor, land, leq]
unaryFunctions = [lneg, ldef]

def singleFunctionTruthTable(func):
	if func in unaryFunctions:
		print(' ' + func.symbol + ' \u2502 .')
		print('\u2500\u2500\u2500\u253c\u2500\u2500\u2500')
		for v in Value:
			print(' ' + v.symbol + ' \u2502 ' + func(v).symbol)
	elif func in functions:
		if len(func.symbol) == 3:
			print(func.symbol + '\u2502', end='')
		elif len(func.symbol) == 2:
			print(' ' + func.symbol + '\u2502', end='')
		else:
			print(' ' + func.symbol + ' \u2502', end='')
		for v in Value:
			print(' ' + v.symbol, end='')
		print()
		print('\u2500'*3 + '\u253c' + '\u2500'*(2*len(Value)+1) )
		for a in Value:
			print(' ' + a.symbol + ' \u2502', end='')
			for b in Value:
				print(' ' + func(a, b).symbol, end='')
			print()

#copied from 'ref.py'
class Ref:

    def __init__(self, val=None):
        self.val = val

    def __eq__(self, value):
        if type(value) is type(self):
            return self.val == value.val
        return self.val == value

    def __ne__(self, value):
        return not self.__eq__(value)

    def __str__(self):
        return 'Reference(' + str(self.val) + ')'

    def __repr__(self):
        return 'Reference(' + repr(self.val) + ')'

def validSentence(sentence: str, system: System) -> bool:
	try:
		letters = getAllLettersInSentence([sentence])
	except AssertionError:
		return False
	try:
		evaluateAtSys(sentence, {c: Value.FALSE for c in letters}, system)
		return True
	except Exception:
		return False
	except AssertionError:
		return False
def validEvalSentence(sentence: str, system: System) -> bool:
	try:
		evaluateSys(sentence, system)
		return True
	except Exception:
		return False
	except AssertionError:
		return False

def evaluateSys(s: str, system: System) -> Value:
	assert s.count('(') == s.count(')')
	ops = [f for f in staticBinaryFunctions]
	assert system in [v for v in System]
	if system == System.PL:
		assert s.count('#') == 0
		ops.append(limpliesK)
		ops.append(liffK)
	elif system == System.K or system == System.LP:
		ops.append(limpliesK)
		ops.append(liffK)
	else:
		ops.append(limpliesL)
		ops.append(liffL)
	def getOp(s, i):
		for f in ops:
			l = len(f.asciiSymbol)
			if i.val + l >= len(s):
				continue
			if s[i.val:i.val+l] == f.asciiSymbol:
				i.val += l
				return f
	def help(s, i, n=False):
		a = None
		assert s[i.val] == '(' or s[i.val] == lneg.asciiSymbol or s[i.val] in [v.symbol for v in Value] or s[i.val] == ldef.asciiSymbol
		if s[i.val] == '(':
			i.val += 1
			a = help(s, i)
			#deal with ')'
			assert s[i.val] == ')'
			i.val += 1 
		elif s[i.val] == lneg.asciiSymbol:
			i.val += 1
			a = lneg(help(s, i, True))
		elif s[i.val] == ldef.asciiSymbol:
			i.val += 1
			a = ldef(help(s, i, True))
		elif s[i.val] in [v.symbol for v in Value]:
			a = getValue(s[i.val])
			i.val += 1
		if n:
			return a
		op = getOp(s, i)
		if op != None:
			b = None
			assert s[i.val] == '(' or s[i.val] == lneg.asciiSymbol or s[i.val] in [v.symbol for v in Value] or s[i.val] == ldef.asciiSymbol
			if s[i.val] == '(':
				i.val += 1
				b = help(s, i)
				#deal with ')'
				assert s[i.val] == ')'
				i.val += 1 
			elif s[i.val] == lneg.asciiSymbol:
				i.val += 1
				b = lneg(help(s, i, True))
			elif s[i.val] == ldef.asciiSymbol:
				i.val += 1
				b = ldef(help(s, i, True))
			elif s[i.val] in [v.symbol for v in Value]:
				b = getValue(s[i.val])
				i.val += 1
			return op(a, b)
		else:
			return a
	
	i = Ref(0)
	val = help(s.replace(' ', ''), i)
	assert i.val == len(s)
	return val

def evaluatePL(s: str) -> Value:
	return evaluateSys(s, System.PL)
def evaluateK(s: str) -> Value:
	return evaluateSys(s, System.K)
def evaluateL(s: str) -> Value:
	return evaluateSys(s, System.L)
def evaluateLP(s: str) -> Value:
	return evaluateSys(s, System.LP)

def evaluateAtSys(s: str, inp: dict, system: System) -> Value:
	for k, v in inp.items():
		s = s.replace(k, v.symbol)
	return evaluateSys(s, system)

def getValidLettersAndOps() -> Tuple[str, str]:
	allLetters = ''.join([chr(ord('A') + i) for i in range(26)] + [chr(ord('a') + i) for i in range(26)])
	opSymbols = '()'
	for f in functions:
		for c in f.asciiSymbol:
			if c not in opSymbols:
				opSymbols += c
	letters = ''
	for c in allLetters:
		if c not in opSymbols:
			letters += c
	return (letters, opSymbols)

def getAllLettersInSentence(ls: list) -> str:
	allLetters, ops = getValidLettersAndOps()
	usedLetters = ''
	for s in ls:
		for c in s.replace(' ', ''):
			assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
			if c in allLetters and c not in usedLetters:
				usedLetters += c
	return ''.join(sorted(usedLetters))

def getStates(length: int) -> str:
	if length <= 0:
		return ''
	elif length == 1:
		for v in Value:
			yield v.symbol
	else:
		for v in Value:
			for s in getStates(length - 1):
				yield v.symbol + s

'''premises is a comma separated list of premises
s is the sentence that is entailed by the premises'''
def entailmentPL(premises: str, s: str) -> Tuple[bool, dict]:
	assert premises.count('#') == 0 and s.count('#') == 0
	premiseList = [p.replace(' ', '') for p in premises.split(',') if p.replace(' ', '') != '']
	def allTrue(l: list) -> bool:
		for x in l:
			if x != Value.TRUE:
				return False
		return True
	allLetters, ops = getValidLettersAndOps()
	usedLetters = ''
	for c in s:
		assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
		if c in allLetters and c not in usedLetters:
			usedLetters += c
	for p in premiseList:
		for c in p:
			assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
			if c in allLetters and c not in usedLetters:
				usedLetters += c
	usedLetters = ''.join(sorted(usedLetters))
	#start evaluating
	for state in getStates(len(usedLetters)):
		if '#' in state:
			continue
		es = s
		for i in range(len(usedLetters)):
			es = es.replace(usedLetters[i], state[i])
		st = evaluatePL(es)
		ept = []
		for ep in premiseList:
			for i in range(len(usedLetters)):
				ep = ep.replace(usedLetters[i], state[i])
			ept.append(evaluatePL(ep))
		if allTrue(ept) and st == Value.FALSE:
			d = {}
			for i in range(len(usedLetters)):
				d[usedLetters[i]] = getValue(state[i])
			return (False, d)
	return (True, None)
def entailmentK(premises: str, s: str) -> Tuple[bool, dict]:
	premiseList = [p.replace(' ', '') for p in premises.split(',') if p.replace(' ', '') != '']
	def allTrue(l: list) -> bool:
		for x in l:
			if x != Value.TRUE:
				return False
		return True
	allLetters, ops = getValidLettersAndOps()
	usedLetters = ''
	for c in s:
		assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
		if c in allLetters and c not in usedLetters:
			usedLetters += c
	for p in premiseList:
		for c in p:
			assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
			if c in allLetters and c not in usedLetters:
				usedLetters += c
	usedLetters = ''.join(sorted(usedLetters))
	#start evaluating
	for state in getStates(len(usedLetters)):
		es = s
		for i in range(len(usedLetters)):
			es = es.replace(usedLetters[i], state[i])
		st = evaluateK(es)
		ept = []
		for ep in premiseList:
			for i in range(len(usedLetters)):
				ep = ep.replace(usedLetters[i], state[i])
			ept.append(evaluateK(ep))
		if allTrue(ept) and st != Value.TRUE:
			d = {}
			for i in range(len(usedLetters)):
				d[usedLetters[i]] = getValue(state[i])
			return (False, d)
	return (True, None)
def entailmentL(premises: str, s: str) -> Tuple[bool, dict]:
	premiseList = [p.replace(' ', '') for p in premises.split(',') if p.replace(' ', '') != '']
	def allTrue(l: list) -> bool:
		for x in l:
			if x != Value.TRUE:
				return False
		return True
	allLetters, ops = getValidLettersAndOps()
	usedLetters = ''
	for c in s:
		assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
		if c in allLetters and c not in usedLetters:
			usedLetters += c
	for p in premiseList:
		for c in p:
			assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
			if c in allLetters and c not in usedLetters:
				usedLetters += c
	usedLetters = ''.join(sorted(usedLetters))
	#start evaluating
	for state in getStates(len(usedLetters)):
		es = s
		for i in range(len(usedLetters)):
			es = es.replace(usedLetters[i], state[i])
		st = evaluateL(es)
		ept = []
		for ep in premiseList:
			for i in range(len(usedLetters)):
				ep = ep.replace(usedLetters[i], state[i])
			ept.append(evaluateL(ep))
		if allTrue(ept) and st != Value.TRUE:
			d = {}
			for i in range(len(usedLetters)):
				d[usedLetters[i]] = getValue(state[i])
			return (False, d)
	return (True, None)
def entailmentLP(premises: str, s: str) -> Tuple[bool, dict]:
	premiseList = [p.replace(' ', '') for p in premises.split(',') if p.replace(' ', '') != '']
	def allNotFalse(l: list) -> bool:
		for x in l:
			if x == Value.FALSE:
				return False
		return True
	allLetters, ops = getValidLettersAndOps()
	usedLetters = ''
	for c in s:
		assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
		if c in allLetters and c not in usedLetters:
			usedLetters += c
	for p in premiseList:
		for c in p:
			assert c in (allLetters + ops + ''.join([v.symbol for v in Value]))
			if c in allLetters and c not in usedLetters:
				usedLetters += c
	usedLetters = ''.join(sorted(usedLetters))
	#start evaluating
	for state in getStates(len(usedLetters)):
		es = s
		for i in range(len(usedLetters)):
			es = es.replace(usedLetters[i], state[i])
		st = evaluateLP(es)
		ept = []
		for ep in premiseList:
			for i in range(len(usedLetters)):
				ep = ep.replace(usedLetters[i], state[i])
			ept.append(evaluateLP(ep))
		if allNotFalse(ept) and st == Value.FALSE:
			d = {}
			for i in range(len(usedLetters)):
				d[usedLetters[i]] = getValue(state[i])
			return (False, d)
	return (True, None)
def entailmentSys(premises: str, s: str, system: System) -> Tuple[bool, dict]:
	if system == System.PL:
		return entailmentPL(premises, s)
	if system == System.K:
		return entailmentK(premises, s)
	if system == System.L:
		return entailmentL(premises, s)
	if system == System.LP:
		return entailmentLP(premises, s)

def validityPL(s: str) -> Tuple[bool, dict]:
	return entailmentPL('', s)
def validityK(s: str) -> Tuple[bool, dict]:
	return entailmentK('', s)
def validityL(s: str) -> Tuple[bool, dict]:
	return entailmentL('', s)
def validityLP(s: str) -> Tuple[bool, dict]:
	return entailmentLP('', s)
def validitySys(s: str, system: System) -> Tuple[bool, dict]:
	return entailmentSys('', s, system)

def prettifySentence(s: str) -> str:
	funcs = sorted(functions, key=lambda f: len(f.asciiSymbol), reverse=True)
	for f in funcs:
		s = s.replace(f.asciiSymbol, f.symbol)
	return s

def defaultSymbols():
	for f in functions:
		f.symbol = f.unicodeSymbol
	lor.symbol = lor.asciiSymbol
	land.symbol = land.asciiSymbol
	ldef.symbol = ldef.asciiSymbol
def unicodeSymbols():
	for f in functions:
		f.symbol = f.unicodeSymbol
def standardSymbols():
	for f in functions:
		f.symbol = f.unicodeSymbol
	ldef.symbol = ldef.asciiSymbol
def asciiSymbols():
	for f in functions:
		f.symbol = f.asciiSymbol

#evaluates at all possible interpretations
#also allows a custom set of letters
def truthOfSys(s: str, system: System, inp: str=None) -> list:
	if system == System.PL:
		assert s.count('#') == 0
	if inp == None:
		usedLetters = getAllLettersInSentence([s])
	else:
		usedLetters = inp
		for c in getAllLettersInSentence([s]):
			if c not in usedLetters:
				usedLetters += c
		usedLetters.sort()
	#start evaluating
	rv = []
	for state in getStates(len(usedLetters)):
		if '#' in state and system == System.PL:
			continue
		es = s
		d = {}
		for i in range(len(usedLetters)):
			es = es.replace(usedLetters[i], state[i])
			d[usedLetters[i]] = getValue(state[i])
		
		rv.append({'truth': evaluateSys(es, system), 'input': d, 'sentence': es})
	return rv

def truthOfPL(s: str, inp: str=None) -> list:
	return truthOfSys(s, System.PL, inp)
def truthOfK(s: str, inp: str=None) -> list:
	return truthOfSys(s, System.K, inp)
def truthOfL(s: str, inp: str=None) -> list:
	return truthOfSys(s, System.L, inp)

'''returns in order hline, vline, cross'''
def getLines(useAscii: bool) -> Tuple[str, str, str]:
	if useAscii:
		return ('-', '|', '|')
	return ('\u2500', '\u2502', '\u253c')

def truthTableSys(s: str, system: System, useAscii: bool=False):
	truthList = truthOfSys(s, system)
	hline, vline, cross = getLines(useAscii)
	if len(truthList) == 0:
		print(f" {prettifySentence(s)}")
		print(hline*(len(prettifySentence(s)) + 2))
		print(' '*((len(prettifySentence(s)) + 1) // 2) + evaluateSys(s, system).symbol)
		return
	letters = getAllLettersInSentence([s])
	pretty = prettifySentence(s)
	lpretty = len(pretty)
	for c in letters:
		print(f' {c} {vline}', end='')
	print(f' {pretty}')
	for c in letters:
		print(f'{hline}{hline}{hline}{cross}', end='')
	print(hline*(2+lpretty))
	for d in truthList:
		for v in d['input'].values():
			print(f' {v.symbol} {vline}', end='')
		dist = (lpretty + 1) // 2
		print(' '*dist + d['truth'].symbol)

def truthTableCompareSys(s1: str, s2: str, system: System, useAscii: bool=False):
	letters = getAllLettersInSentence([s1, s2])
	truthList1 = truthOfSys(s1, system, letters)
	truthList2 = truthOfSys(s2, system, letters)
	assert len(truthList1) == len(truthList2)
	hline, vline, cross = getLines(useAscii)
	pretty1 = prettifySentence(s1)
	pretty2 = prettifySentence(s2)
	if len(truthList1) == 0:
		print(f" {pretty1} {vline} {pretty2}")
		print(hline*(len(pretty1) + 2) + cross + hline*(len(pretty2) + 2))
		print(' '*((len(pretty1) + 1) // 2) + evaluateSys(s1, system).symbol + ' '*((len(pretty1) + 1) // 2) + (' ' if len(pretty1) % 2 == 0 else '') + vline, end='')
		print(' '*((len(pretty2) + 1) // 2) + evaluateSys(s2, system).symbol)
		return
	for c in letters:
		print(f' {c} {vline}', end='')
	print(f' {pretty1} {vline} {pretty2}')
	for c in letters:
		print(f'{hline}{hline}{hline}{cross}', end='')
	print(hline*(2+len(pretty1)) + cross + hline*(2+len(pretty2)))
	for i in range(len(truthList1)):
		for v in truthList1[i]['input'].values():
			print(f' {v.symbol} {vline}', end='')
		dist1 = (len(pretty1) + 1) // 2
		dist2 = (len(pretty2) + 1) // 2
		print(' '*dist1 + truthList1[i]['truth'].symbol + ' '*dist1 + (' ' if len(pretty1) % 2 == 0 else '') + vline, end='')
		print(' '*dist2 + truthList2[i]['truth'].symbol)
