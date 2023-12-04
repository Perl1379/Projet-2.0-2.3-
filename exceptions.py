'''fichier des erreurs'''
class ErreurDate(RuntimeError):
    '''probleme d'une date inutilisable'''
    def __str__(self):
        return f'Erreur Date: {self.args}'


class ErreurQuantité(RuntimeError):
    '''probleme d'une quantité insuffisante'''
    def __str__(self):
        return f'Erreur Quantité: {self.args}'


class LiquiditéInsuffisante(RuntimeError):
    '''probleme de font insuffisant'''
    def __str__(self):
        return f'Liquidité Insuffisante: {self.args}'
