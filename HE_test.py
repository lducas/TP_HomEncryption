from HE_sol import *
from random import randint


def Check_Enc_WellFormed(n, c):
    (a, b) = c
    (nn,) = a.shape
    if n!=nn:
        raise ValueError("Le chiffre est mal forme: la dimension de a differe de la dimension du secret s")

    for x in (list(a)+[b]):
        if not (isinstance(x, int) and x >= 0 and x < q):
            raise ValueError("Le chiffre est mal forme: ses valeurs ne sont pas des entiers dans [0, q-1]")


def test_EncDec(N):
    print "==== TESTING ENC/DEC ===="
    for i in range(N):
        s = KeyGen(10)
        mu = randint(0, 1)
        c = Enc(s, mu)
        Check_Enc_WellFormed(10, c)
        mu2 = Dec(s, c)
        print "Dec( Enc(%d) ) = %d"%(mu, mu2)

        if mu != mu:
            raise ValueError("Le dechiffrement n'est pas correcte.")

    print "SUCCESS !"


test_EncDec(10)


def test_HomNOT(N):
    print "==== TESTING HomNOT ===="

    for i in range(N):
        s = KeyGen(10)
        mu = randint(0, 1)
        c = Enc(s, mu)
        cc = HomNOT(c)
        Check_Enc_WellFormed(10, cc)
        mu2 = Dec(s, cc)
        print "Dec( homNOT Enc(%d) ) = %d"%(mu, mu2)

        if mu2 != 1-mu:
            raise ValueError("Le dechiffrement apres homNOT n'est pas correcte.")

    print "SUCCESS !"

test_HomNOT(10)

def test_HomXOR(N):
    print "==== TESTING HomXOR ===="

    for i in range(N):
        s = KeyGen(10)
        mu1 = randint(0, 1)
        c1 = Enc(s, mu1)
        mu2 = randint(0, 1)
        c2 = Enc(s, mu2)

        cc = HomXOR(c1, c2)
        Check_Enc_WellFormed(10, cc)
        mu3 = Dec(s, cc)

        print "Dec( Enc(%d) homXOR Enc(%d)) = %d"%(mu1, mu2, mu3)
        if mu3 != mu1^mu2:
            raise ValueError("Le dechiffrement apres homXOR n'est pas correcte.")

    print "SUCCESS !"

test_HomXOR(10)


def test_HomAND(N):
    print "==== TESTING HomAND ===="

    for i in range(N):
        s = KeyGen(10)
        mu1 = randint(0, 1)
        c1 = Enc(s, mu1)
        mu2 = randint(0, 1)
        c2 = Enc(s, mu2)

        ss = tensored_key(s)
        cc = HomAND(c1, c2)

        Check_Enc_WellFormed(120, cc)
        mu3 = Dec(ss, cc)
        print "Dec( Enc(%d) homAND Enc(%d)) = %d"%(mu1, mu2, mu3)
        if mu3 != mu1 & mu2:
            raise ValueError("Le dechiffrement apres homAND n'est pas correcte.")

    print "SUCCESS !"

test_HomAND(10)


def test_KeySwitch(N):
    print "==== TESTING KeySwitch ===="

    for i in range(N):
        s1 = KeyGen(50)
        s2 = KeyGen(10)
        K = KeySwitchGen(s1, s2)
        mu1 = randint(0, 1)
        c1 = Enc(s1, mu1)
        c2 = KeySwitch(K, c1)

        Check_Enc_WellFormed(10, c2)
        mu2 = Dec(s2, c2)
        print "Dec_s2( KeySwitch(Enc_s1(%d)) = %d"%(mu1, mu2)
        if mu2 != mu1:
            raise ValueError("Le dechiffrement apres KeySwitch n'est pas correcte.")

    print "SUCCESS !"

test_KeySwitch(10)