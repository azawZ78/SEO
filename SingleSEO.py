import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv
import string
from urllib.parse import urlparse

# Fonction pour obtenir le contenu HTML d'une URL
def obtenir_contenu_html(url):
    reponse = requests.get(url)
    return reponse.text

# Fonction pour retirer les balises HTML d'un texte
def retirer_balises_html(texte):
    soup = BeautifulSoup(texte, 'html.parser')
    return soup.get_text()

# Fonction pour obtenir les occurrences des mots dans un texte
def obtenir_occurrences_mots(texte):
    mots = [mot.strip(''.join(char for char in string.punctuation)) for mot in texte.split()]
    return dict(sorted(Counter(mots).items(), key=lambda item: item[1], reverse=True))

# Fonction pour retirer les mots parasites d'une liste d'occurrences de mots
def retirer_mots_parasites(occurrences_mots, mots_parasites):
    return {mot: compte for mot, compte in occurrences_mots.items() if mot.lower() not in map(str.lower, mots_parasites)}

# Fonction pour obtenir les valeurs d'attributs d'une balise dans un texte HTML
def obtenir_valeurs_attributs(html, nom_balise, nom_attribut):
    soup = BeautifulSoup(html, 'html.parser')
    return [balise[nom_attribut] for balise in soup.find_all(nom_balise) if nom_attribut in balise.attrs]

# Fonction pour extraire le nom de domaine à partir d'une URL
def extraire_nom_domaine(url):
    return urlparse(url).netloc

# Fonction pour filtrer les URLS par domaine
def filtrer_urls_par_domaine(domaine, liste_urls):
    urls_domaine = [url for url in liste_urls if extraire_nom_domaine(url) == domaine]
    return urls_domaine, [url for url in liste_urls if url not in urls_domaine]

# Fonction pour effectuer l'audit SEO
def audit_seo():
    url = input("Veuillez entrer l'URL à analyser : ")
    contenu_html = obtenir_contenu_html(url)
    texte_sans_balises = retirer_balises_html(contenu_html)
    
    occurrences_mots = obtenir_occurrences_mots(texte_sans_balises)
    mots_parasites = [mot.strip() for mot in open('parasite.csv', 'r', encoding='utf-8').readlines()]

    occurrences_mots_filtrees = retirer_mots_parasites(occurrences_mots, mots_parasites)
    img_alt_values = obtenir_valeurs_attributs(contenu_html, 'img', 'alt')
    
    liens = obtenir_valeurs_attributs(contenu_html, 'a', 'href')
    liens_domaine, liens_non_domaine = filtrer_urls_par_domaine(extraire_nom_domaine(url), liens)

    print(f"Audit SEO pour {url} :")
    print("Occurrences des mots-clés :")
    for mot, compte in list(occurrences_mots_filtrees.items())[:3]:
        print(f"{mot} : {compte} occurrences")

    print(f"Nombre de liens entrants : {len(liens_domaine)}")
    print(f"Nombre de liens sortants : {len(liens_non_domaine)}")
    print(f"Valeurs Alt pour les images : {len(img_alt_values)}")

# Exécutez la fonction pour lancer l'audit avec l'URL fournie par l'utilisateur
audit_seo()