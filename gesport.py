import datetime
import argparse
import exceptions
import phase1
import bourse
import portefeuille


def analyser_commande():
    '''fonction qui genere un interpreteur de commande'''
    parser = argparse.ArgumentParser(description='{déposer,acheter,vendre,lister,projeter}')
    subparser = parser.add_subparsers(title='ACTION', help="Gestionnaire de portefeuille d'actions", dest='monSubparser')
    parser_d = subparsers.add_parser('déposer', help='À la date spécifiée, déposer la quantité de dollars spécifiée')
    parser_d.add_argument('-d', '--date', metavar='DATE', dest='date',
    help='Date effective (par défaut, date du jour)', default=datetime.date.today())
    parser_d.add_argument('-q', '--quantité', metavar='INT', dest='quantite',
    help='Quantité désirée (par défaut: 1)', default=1)
    parser_d.add_argument('-t', '--titres', metavar='STRING [STRING [STRING ...]]', dest='titres',
    help='Le ou les titres à considérer (par défaut, tous les titres du portefeuille sont considérés)')
    parser_d.add_argument('-r', '--rendement', metavar='FLOAT', dest='rendement',
    help='Rendement annuel global (par défaut, 0)', default=0)
    parser_d.add_argument('-v', '--volatilité', metavar='FLOAT', dest='volatilite',
    help='Indice de volatilité global sur le rendement annuel(par défaut, 0)', default=0)
    parser_d.add_argument('-g', '--graphique', metavar='BOOL', dest='graphique',
    help="Affichage graphique (par défaut, pas d'affichage graphique)", default=None)
    parser_d.add_argument('-p', '--portefeuille', metavar='STRING', dest='portefeuille',
    help='Nom de portefeuille (par défaut, utiliser folio)', default='folio')
    parser_a = subparsers.add_parser('acheter', help='À la date spécifiée, acheter la quantité spécifiée des titres spécifiés')
    parser_a.add_argument('-d', '--date', metavar='DATE', dest='date',
    help='Date effective (par défaut, date du jour)', default=datetime.date.today())
    parser_a.add_argument('-q', '--quantité', metavar='INT', dest='quantite',
    help='Quantité désirée (par défaut: 1)', default=1)
    parser_a.add_argument('-t', '--titres', metavar='STRING [STRING [STRING ...]]', dest='titres',
    help='Le ou les titres à considérer (par défaut, tous les titres du portefeuille sont considérés)')
    parser_a.add_argument('-r', '--rendement', metavar='FLOAT', dest='rendement',
    help='Rendement annuel global (par défaut, 0)', default=0)
    parser_a.add_argument('-v', '--volatilité', metavar='FLOAT', dest='volatilite',
    help='Indice de volatilité global sur le rendement annuel(par défaut, 0)', default=0)
    parser_a.add_argument('-g', '--graphique', metavar='BOOL', dest='graphique',
    help="Affichage graphique (par défaut, pas d'affichage graphique)", default=None)
    parser_a.add_argument('-p', '--portefeuille', metavar='STRING', dest='portefeuille',
    help='Nom de portefeuille (par défaut, utiliser folio)', default='folio')
    parser_v = subparsers.add_parser('vendre', help='À la date spécifiée, vendre la quantité spécifiée des titres spécifiés')
    parser_v.add_argument('-d', '--date', metavar='DATE', dest='date',
    help='Date effective (par défaut, date du jour)', default=datetime.date.today())
    parser_v.add_argument('-q', '--quantité', metavar='INT', dest='quantite',
    help='Quantité désirée (par défaut: 1)', default=1)
    parser_v.add_argument('-t', '--titres', metavar='STRING [STRING [STRING ...]]', dest='titres',
    help='Le ou les titres à considérer (par défaut, tous les titres du portefeuille sont considérés)')
    parser_v.add_argument('-r', '--rendement', metavar='FLOAT', dest='rendement',
    help='Rendement annuel global (par défaut, 0)', default=0)
    parser_v.add_argument('-v', '--volatilité', metavar='FLOAT', dest='volatilite',
    help='Indice de volatilité global sur le rendement annuel(par défaut, 0)', default=0)
    parser_v.add_argument('-g', '--graphique', metavar='BOOL', dest='graphique',
    help="Affichage graphique (par défaut, pas d'affichage graphique)", default=None)
    parser_v.add_argument('-p', '--portefeuille', metavar='STRING', dest='portefeuille',
    help='Nom de portefeuille (par défaut, utiliser folio)', default='folio')
    parser_l = subparsers.add_parser('lister', help="À la date spécifiée, pour chacun des titres spécifiés, lister les nombres d'actions détenues ainsi que leur valeur totale")
    parser_l.add_argument('-d', '--date', metavar='DATE', dest='date',
    help='Date effective (par défaut, date du jour)', default=datetime.date.today())
    parser_l.add_argument('-q', '--quantité', metavar='INT', dest='quantite',
    help='Quantité désirée (par défaut: 1)', default=1)
    parser_l.add_argument('-t', '--titres', metavar='STRING [STRING [STRING ...]]', dest='titres',
    help='Le ou les titres à considérer (par défaut, tous les titres du portefeuille sont considérés)')
    parser_l.add_argument('-r', '--rendement', metavar='FLOAT', dest='rendement',
    help='Rendement annuel global (par défaut, 0)', default=0)
    parser_l.add_argument('-v', '--volatilité', metavar='FLOAT', dest='volatilite',
    help='Indice de volatilité global sur le rendement annuel(par défaut, 0)', default=0)
    parser_l.add_argument('-g', '--graphique', metavar='BOOL', dest='graphique',
    help="Affichage graphique (par défaut, pas d'affichage graphique)", default=None)
    parser_l.add_argument('-p', '--portefeuille', metavar='STRING', dest='portefeuille',
    help='Nom de portefeuille (par défaut, utiliser folio)', default='folio')
    parser_p = subparsers.add_parser('lister', help='À la date future spécifiée, projeter la valeur totale des titres spécifiés, en tenant compte des rendements et indices de volatilité spécifiés')
    parser_p.add_argument('-d', '--date', metavar='DATE', dest='date',
    help='Date effective (par défaut, date du jour)', default=datetime.date.today())
    parser_p.add_argument('-q', '--quantité', metavar='INT', dest='quantite',
    help='Quantité désirée (par défaut: 1)', default=1)
    parser_p.add_argument('-t', '--titres', metavar='STRING [STRING [STRING ...]]', dest='titres',
    help='Le ou les titres à considérer (par défaut, tous les titres du portefeuille sont considérés)')
    parser_p.add_argument('-r', '--rendement', metavar='FLOAT', dest='rendement',
    help='Rendement annuel global (par défaut, 0)', default=0)
    parser_p.add_argument('-v', '--volatilité', metavar='FLOAT', dest='volatilite',
    help='Indice de volatilité global sur le rendement annuel(par défaut, 0)', default=0)
    parser_p.add_argument('-g', '--graphique', metavar='BOOL', dest='graphique',
    help="Affichage graphique (par défaut, pas d'affichage graphique)", default=None)
    parser_p.add_argument('-p', '--portefeuille', metavar='STRING', dest='portefeuille',
    help='Nom de portefeuille (par défaut, utiliser folio)', default='folio')
    return parser.parse_args()

if not argpars.titres:
    for titre in titres:
        argpars.titres.append(titre) 