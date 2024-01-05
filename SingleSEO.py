import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv
import string
from urllib.parse import urlparse

# Etape 1
def obtenir_occurrences_mots(texte):
    mots = texte.split()
    mots = [mot.strip(string.punctuation) for mot in mots]
    occurrences_mots = Counter(mots)
    occurrences_mots_triees = dict(sorted(occurrences_mots.items(), key=lambda item: item[1], reverse=True))
    return occurrences_mots_triees

# Etape 2
def retirer_mots_vides(occurrences_mots, mots_vides):
    mots_vides_lower = set(mot.lower() for mot in mots_vides)
    return {mot: compte for mot, compte in occurrences_mots.items() if mot.lower() not in mots_vides_lower}

# Etape 3
def obtenir_mots_vides_de_fichier(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        mots_vides = [ligne.strip() for ligne in fichier]
    return mots_vides

# Etape 5
def retirer_balises_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

# Etape 6
def obtenir_valeurs_attributs(html, nom_balise, nom_attribut):
    soup = BeautifulSoup(html, 'html.parser')
    return [balise[nom_attribut] for balise in soup.find_all(nom_balise) if nom_attribut in balise.attrs]

# Etape 8
def extraire_nom_domaine(url):
    url_parsee = urlparse(url)
    return url_parsee.netloc

# Etape 9
def filtrer_urls_par_domaine(domaine, liste_urls):
    urls_domaine = [url for url in liste_urls if extraire_nom_domaine(url) == domaine]
    urls_non_domaine = [url for url in liste_urls if extraire_nom_domaine(url) != domaine]
    return urls_domaine, urls_non_domaine

# Etape 10
def obtenir_contenu_html(url):
    reponse = requests.get(url)
    return reponse.text

# Etape 11
def audit_seo():
    url = input("Veuillez entrer l'URL à analyser : ")
    contenu_html = obtenir_contenu_html(url)

    # Etape 5
    texte_sans_balises = retirer_balises_html(contenu_html)

    # Etape 1
    occurrences_mots = obtenir_occurrences_mots(texte_sans_balises)

    # Etape 3
    mots_vides = obtenir_mots_vides_de_fichier('parasite.csv')

    # Etape 2
    occurrences_mots_filtrees = retirer_mots_vides(occurrences_mots, mots_vides)

    # Etape 6
    img_alt_values = obtenir_valeurs_attributs(contenu_html, 'img', 'alt')

    # Etape 9
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