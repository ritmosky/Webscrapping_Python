
########## BIBLIOTHEQUES ##########


# bibliothèque pour faire des requêts HTTP
import requests

# bibliothèque pour parser le code HTML
from bs4 import BeautifulSoup

# bibliothèque pour charger les données
import csv

import os


########## FIRST STEP ##########


# url du site qu'on veut analyser
url = "https://www.gov.uk/search/news-and-communications"


# on recupère le code source HTML de la page
page = requests.get(url)


# voir le code source HTML
page.content


# objet contenant les fonctions pour parser
soup = BeautifulSoup(page.content, 'html.parser')


soup.title  # récupérer titre de la page
print(soup.title.string)

soup.find(id="s") # tous les éléments dont id="s"
soup.find_all("p") # liste de tous les paragraphes
soup.find_all("a") # liste de tous les liens


########## RECUPERATION DES ELEMENTS ##########
""" récupérer les titres de toutes les histoires. Après avoir inspecté la page HTML
- titres sont dans <a class='gem-c-document-list__item-title' ...
- descriptions dans dans <a class='gem-c-document-list__item-description' ...
"""


# trouver class et id des éléments à extraire
titres_bs = soup.find_all("a", class_="gem-c-document-list__item-title")
titres = []
for titre in titres_bs:
    titres.append(titre.string)


descriptions_bs = soup.find_all("p", class_="gem-c-document-list__item-description")
descriptions = []
for desc in descriptions_bs:
    descriptions.append(desc.string)   # conversion au format str et ajout dans liste


########## CHARGEMENT DES DONNEES AVEC CSV ##########
# go to the folder if using a ide
os.getcwd()
os.chdir("Documents/python/extraction_web/UK_news")


# entête du fichier
en_tete=["Titre", "Description"]


with open("data_news.csv", "w") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(en_tete)

    for t, d in zip(titres, descriptions):
        ligne=[t, d]
        writer.writerow(ligne)


########## SOUS FORME DE FONCTION ##########


# récupère les titres ou descriptions comme liste de strings
def extraire_donnees(l):
   res = []
   for e in l:
      res.append(e.string)
   return res


# charger la donnée dans un fichier csv
def charger_donnees(nom_fichier, en_tete, titres, descriptions):
   with open(nom_fichier, 'w') as fichier_csv:
      writer = csv.writer(fichier_csv, delimiter=',')
      writer.writerow(en_tete)
      for titre, description in zip(titres, descriptions):
         writer.writerow([titre, description])



def etl():
   # lien de la page à scrapper
   url = "https://www.gov.uk/search/news-and-communications"
   page = requests.get(url)

   # transforme (parse) le HTML en objet BeautifulSoup
   soup = BeautifulSoup(page.content, "html.parser")

   # récupération de tous les titres
   titres = soup.find_all("a", class_="gem-c-document-list__item-title")

   # récupération de toutes les descriptions
   descriptions = soup.find_all("p", class_="gem-c-document-list__item-description")

   en_tete = ["title", "description"]
   titres = extraire_donnees(titres)
   descriptions = extraire_donnees(descriptions)
   charger_donnees("data.csv", en_tete, titres, descriptions)


etl()

