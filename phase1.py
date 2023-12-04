'''programme de recherche d'historique boursiere'''
import argparse
import json
import datetime
import requests

def analyser_commande():
    '''fonction qui genere un interpreteur de commande'''
    parser = argparse.ArgumentParser(
    description='Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.')
    
    parser.add_argument('symbole', nargs='+',
    help="Nom d'un symbole boursier")
    
    parser.add_argument('-d', '--debut', metavar='DATE', dest='debut',
    help='Date recherchée la plus ancienne (format: AAAA-MM-JJ)')
    
    parser.add_argument('-f', '--fin', metavar='DATE', dest='fin',
    default=str(datetime.date.today()),
    help='Date recherchée la plus récente (format: AAAA-MM-JJ)')
    
    parser.add_argument('-v', '--valeur', dest='valeur', default='fermeture',
    choices=['fermeture', 'ouverture', 'min', 'max', 'volume'],
    help='La valeur désirée (par défaut: fermeture)',)
    
    return parser.parse_args()

# args = analyser_commande()
# if args.debut is None:
#     args.debut = args.fin

def produire_historique(symbole, debut, fin, valeur):
    '''fonction qui trouve l'historique boursiere'''
    liste = []  
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    params = {'début': str(debut), 'fin': str(fin)}
    reponse = requests.get(url=url, params=params)
    reponse = json.loads(reponse.text)
    if "message d'erreur" in reponse:
        return reponse
    for i, j in sorted(reponse['historique'].items()):
        liste.append(tuple((datetime.datetime.strptime(i, '%Y-%m-%j').date(), j[valeur])))
    return liste

#for symbole in args.symbole:
#    print(f'titre={symbole}, : valeur={args.valeur}, début={args.debut}, fin={args.fin}')
#    print(str(produire_historique(symbole, args.debut, args.fin, args.valeur)))

#print(produire_historique('a', datetime.date.today(), datetime.date.today(), 'fermeture'))