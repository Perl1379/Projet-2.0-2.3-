'''fichier qui accède à la bourse'''
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
        return produire_historique(symbole, date, date, 'fermeture')[0][1]
