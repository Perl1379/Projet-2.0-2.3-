from phase1 import produire_historique
from datetime import *
from exceptions import *

class Bourse:
    def prix(symbole, date):
        '''donne le prix d'une action à une date'''
        if date > date.today():
            raise ErreurDate()
        while not produire_historique(symbole, date, date, 'fermeture'):
            date = date - timedelta(days=1)
        #print(produire_historique(symbole, date, date, 'fermeture'))
        return produire_historique(symbole, date, date, 'fermeture')[0][1]

#print(Bourse.prix('goog', date.today()))