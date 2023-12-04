'''fichier qui accède au portefeuille'''
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


    def solde(self, date=date.today()):
        '''retourne le montant total dans liquidité'''
        if date > date.today():
            raise ErreurDate()
        total = 0
        for i in self.liquidité.keys():
            if i <= date:
                total += self.liquidité[i]
        return total


    def acheter(self, symbole, quantité, date=date.today()):
        '''achète une action à la bourse'''
        if date > date.today():
            raise ErreurDate()
        if self.solde(date) < self.bourse.prix(symbole, date)*quantité:
            raise LiquiditéInsuffisante()
        self.déposer(-self.bourse.prix(symbole, date)*quantité, date)
        if not self.action.get(date, None):
            self.action[date] = {symbole: quantité}
        else:
            if not self.action[date].get(symbole, None):
                self.action[date][symbole] = quantité
            else:
                self.action[date][symbole] += quantité


    def vendre(self, symbole, quantité, date=date.today()):
        '''vend une action du portefeuille'''
        if date > date.today():
            raise ErreurDate()
        if self.titres(date).get(symbole, 0) < quantité:
            raise ErreurQuantité()
        self.déposer(self.bourse.prix(symbole, date)*quantité, date)
        if not self.action.get(date, None):
            self.action[date] = {symbole: -quantité}
        else:
            if not self.action[date].get(symbole, None):
                self.action[date][symbole] = -quantité
            else:
                self.action[date][symbole] -= quantité


    def valeur_totale(self, date=date.today()):
        '''retourne la valeure totale du portefeuille'''
        if date > date.today():
            raise ErreurDate()
        valeur_action = 0
        for s in self.titres(date):
            valeur_action += self.bourse.prix(s, date)*self.titres(date)[s]
        return self.solde(date) + valeur_action


    def valeur_des_titres(self, symboles, date=date.today()):
        '''retourne la valeure des actions du portefeuille'''
        if date > date.today():
            raise ErreurDate()
        total_titres = 0
        for s in symboles:
            total_titres += self.bourse.prix(s, date)*self.titres(date)[s]
        return total_titres


    def titres(self, date=date.today()):
        '''retourne le nombre d'action de chaque titre'''
        if date > date.today():
            raise ErreurDate()
        Titres = {}
        for d in self.action.keys():
            if d <= date:
                for s in self.action[d].keys():
                    if not Titres.get(s, None):
                        Titres[s] = self.action[d][s]
                    else:
                        Titres[s] += self.action[d][s]
        return Titres


    def valeur_projetée(self, date, rendement):
        '''retourne la valeure du portefeuille à un temps future après un rendement'''
        temps = date - date.today()
        ans = temps.days // 365
        jours = temps.days % 365
        solde_action = {}
        for s in self.titres():
            solde_action[s] = self.valeur_des_titres([s])
            if isinstance(rendement, dict):
                solde_action[s] = (solde_action[s]*(1+rendement.get(s, 0)/100)**ans +
                solde_action[s]*(jours/365)*(rendement.get(s, 0)/100))
            if isinstance(rendement, float):
                solde_action[s] = (solde_action[s]*(1+rendement/100)**ans +
                solde_action[s]*(jours/365)*(rendement/100))
        valeur_action = 0
        for a in solde_action.keys():
            valeur_action += solde_action[a]
        return self.solde() + valeur_action
