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
        
    def valeur_totale(self, date=date.today()):
        '''retourne la valeure totale du portefeuille'''
        if date > date.today():
            raise ErreurDate()
        valeur_action = 0
        for s in self.titres(date):
            valeur_action += self.bourse.prix(s, date)*self.titres(date)[s]
        #print(self.solde(date) + valeur_action)
        return self.solde(date) + valeur_action
        
    
    def valeur_des_titres(self, symboles, date=date.today()):
        '''retourne la valeure des actions du portefeuille'''
        if date > date.today():
            raise ErreurDate()
        Valeur_des_titres = 0
        for s in symboles:
            Valeur_des_titres += self.bourse.prix(s, date)*self.titres(date)[s]
        #print(Valeur_des_titres)
        return Valeur_des_titres
    
    def titres(self, date=date.today()):
        '''retourne le nombre d'action de chaque titre'''
        if date > date.today():
            raise ErreurDate()
        Titres = {}
        for d in self.action:
            if d <= date:
                for s in self.action[d]:
                    if not Titres.get(s, None):
                        Titres[s] = self.action[d][s]
                    else:
                        Titres[s] += self.action[d][s]
        #print(Titres)
        return Titres
    
    def valeur_projetée(self, date, rendement):
        '''retourne la valeure du portefeuille à un temps future après un rendement'''
        temps = date - date.today()
        ans = temps.days // 365
        jours = temps.days % 365
        solde_action = {}
        for s in self.titres():
            solde_action[s] = self.valeur_des_titres([s])
            if type(rendement) is dict:
                solde_action[s] = (solde_action[s]*(1+rendement.get(s, 0)/100)**ans + solde_action[s]*(jours/365)*(rendement.get(s, 0)/100))
            if type(rendement) is float:
                solde_action[s] = (solde_action[s]*(1+rendement/100)**ans + solde_action[s]*(jours/365)*(rendement/100))
        #print(solde_action)
        Valeur_action = 0
        for S in solde_action:
            Valeur_action += solde_action[S]
        #print(Valeur_action)
        return self.solde() + Valeur_action


# p = Portefeuille(Bourse)
# Portefeuille.déposer(p, 1000, date(2021, 2, 14))
# Portefeuille.déposer(p, 1000, date(2021, 10, 14))
# Portefeuille.solde(p, date(2021, 3, 14))
# Portefeuille.acheter(p,'a', 2)
# Portefeuille.acheter(p,'aapl', 7)
# Portefeuille.acheter(p,'a', 2, date(2021, 2, 14))
# Portefeuille.titres(p)
# Portefeuille.valeur_des_titres(p, ['aapl', 'a'])
# Portefeuille.valeur_projetée(p, date(2024, 1, 2), {'a': 20, 'aapl': 0.4})
# Portefeuille.vendre(p,'a', 2)
# Portefeuille.vendre(p,'aapl', 7)
# Portefeuille.vendre(p,'a', 2, date(2021, 2, 20))
# Portefeuille.valeur_totale(p, date(2021, 9, 14))
# Portefeuille.valeur_projetée(p, date(2024, 12, 14), 0.4)