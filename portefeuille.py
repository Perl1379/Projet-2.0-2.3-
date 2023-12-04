from datetime import *
from exceptions import *
from bourse import *

class Portefeuille(Bourse):
    '''ensemble des fonctions qui permettent la gestion d'un posrtefeuille d'actions'''
    def __init__(self, bourse):
        '''initialise les variables'''
        self.bourse = bourse
        self.liquidité = {}
        self.action = {}

    def déposer(self, montant, date=date.today()):
        '''dépose un montant dans liquidité'''
        if date > date.today():
            raise ErreurDate()
        if not self.liquidité.get(date, None):
            self.liquidité[date] = montant
        else:
            self.liquidité[date] += montant
        #print(self.liquidité)
    
    def solde(self, date=date.today()):
        '''retourne le montant total dans liquidité'''
        if date > date.today():
            raise ErreurDate()
        Solde = 0
        for i in self.liquidité:
            if i <= date:
                Solde += self.liquidité[i]
        #print(Solde)
        return Solde

    def acheter(self, symbole, quantité, date=date.today()):
        '''achète une action à la bourse'''
        if date > date.today():
            raise ErreurDate()
        if self.solde(date) < self.bourse.prix(symbole, date)*quantité:
            raise LiquiditéInsuffisante()
        self.déposer(-self.bourse.prix(symbole, date)*quantité, date)
        #print(self.liquidité)
        if not self.action.get(date, None):
            self.action[date] = {symbole: quantité}
        else:
            if not self.action[date].get(symbole, None):
                self.action[date][symbole] = quantité
            else:
                self.action[date][symbole] += quantité
        #print(self.action)

    def vendre(self, symbole, quantité, date=date.today()):
        '''vend une action du portefeuille'''
        if date > date.today():
            raise ErreurDate()
        if self.titres(date).get(symbole, 0) < quantité:
            raise ErreurQuantité()
        self.déposer(self.bourse.prix(symbole, date)*quantité, date)
        #print(self.liquidité)
        if not self.action.get(date, None):
            self.action[date] = {symbole: -quantité}
        else:
            if not self.action[date].get(symbole, None):
                self.action[date][symbole] = -quantité
            else:
                self.action[date][symbole] -= quantité
        #print(self.action)