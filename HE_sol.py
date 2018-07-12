from numpy import array
from random import randint
from math import log, ceil

q = 1001
k = int(ceil(log(q)/log(2)))
B = 5


def balanced_modq(x):
	'''
	reduit x modulo q, dans l'interval [-q/2, q/2]
	'''
	y = x % q
	if y > q/2:
		y -= q
	return y

def KeyGen(n):
	'''
	Genere une clef secrete (vecteur uniform de dimension n modulo q)
	'''
	s = array([randint(0, q-1) for i in range(n)])
	return s

def Enc(s, mu):
	'''
	Retourne un chiffre c = (a, b) du message s sous la clef mu	
	'''

	(n,) = s.shape
	a = array([randint(0, q-1) for i in range(n)])
	e = randint(-B, B)
	b = (s.dot(a) + 2 * e + mu) % q
	return (a, b)

def Dec(s, c):
	'''
	Dechiffre un chiffre c = (a, b) avec la clef s
	'''
	(a, b) = c
	d = balanced_modq(b - a.dot(s))
	mu = d % 2
	return mu

def HomNOT(c):
	'''
	Applique la porte NOT homomorphiquement a un chiffre
	'''
	(a, b) = c
	return (a, (b+1) % q)


def HomXOR(c1, c2):
	'''
	Applique la porte XOR homomorphiquement a deux chiffre
	'''
	(a1, b1) = c1
	(a2, b2) = c2
	return ((a1 + a2) % q, (b1 + b2) % q)

def tensored_key(s):
	'''
	Calcul la `clef tenseur', cad la nouvelle clef apres l'application de HomAND
	'''
	(n,) = s.shape
	L = []
	for i in range(n):
		for j in range(n):
			L += [- s[i] * s[j]]

	for j in range(n):
		L += [s[j]]

	for j in range(n):
		L += [s[j]]

	ts = array(L) % q
	return ts

def HomAND(c1, c2):
	'''
	Applique la porte XOR homomorphiquement a deux chiffre.
	(La nouvelle clef est implicitement devenue tensored_key(s) 
	ou s est la clef originale.)
	'''
	(a1, b1) = c1
	(a2, b2) = c2

	(n,) = a1.shape
	L = []
	for i in range(n):
		for j in range(n):
			L += [a1[i] * a2[j]]

	for j in range(n):
		L += [b1 * a2[j]]

	for j in range(n):
		L += [b2 * a1[j]]

	a = array(L) % q
	b = (b1 * b2) % q

	return (a, b)

def KeySwitchGen(s1, s2):
	'''
	Genere une KeySwitching Key de la clef s1 vers la clef s2
	'''
	K = {}
	(n1,) = s1.shape
	for i in range(n1):
		for j in range(k):
			K[(i, j)] = Enc(s2, 2**j * s1[i])

	return K

def BitDecomp(x):
	L = []
	for i in range(k):
		L += [x % 2]
		x /= 2
	return L

def KeySwitch(K, c):
	'''
	Transform un chiffre sous la clef s1 en un chiffre sous la clef s2
	'''
	(a, b) = c
	(n1,) = a.shape
	(n2,) = K[(0,0)][0].shape

	aa = array([0 for i in range(n2)])
	bb = b
		
	for i in range(n1):
		L = BitDecomp(a[i])
		for j in range(k):
			(Ka, Kb) = K[(i, j)]
			aa = (aa - L[j] * Ka) % q
			bb = (bb - L[j] * Kb) % q

	return (aa, bb)	

