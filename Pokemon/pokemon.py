

########## BIBLIOTHEQUES ##########


# pour manipuler les dataframes
import pandas as pd

# bibliothèque pour parser le code HTML
from bs4 import BeautifulSoup

# faire des requêts HTTP
import requests

# fichier YAML en entrée et analysera le HTML
import selectorlib
from selectorlib import Extractor

import os

########## CHARGEMENT DE LA PAGE ##########
# https://www.site.com/robots.txt -> info sur l'extraction de données


# vérifier si le site est extractible
def url_checker(URL):
    try:
        # récupérer la page
        PAGE = requests.get(URL)
        # si requête a réussi
        if PAGE.status_code == 200:
            return(f"# {URL} # : is << REACHABLE >>")
        else:
            return(f"# {URL} # : is << NOT REACHABLE >>, status_code: {PAGE.status_code}")

    # Exception
    except requests.exceptions.ConnectionError as e:
        # arrêter la procédure
        #raise SystemExit(f"# {URL} #: is << NOT REACHABLE >> \nErr: {e}")
        raise e


url = "https://scrapeme.live/shop/"

#url = input("\n Entrer le lien de l'objet à surveiller : ")
print(url_checker(url))

# ouverture de la page
page = requests.get(url)



# charement de la page et affichage du titre  html.parser lxml html5lib
soup = BeautifulSoup(page.content, 'lxml')
print(soup.prettify())
print("==>", soup.title.string, "<==")


########## EXTRACTIONS DES ELEMENTS D'UNE PAGE ##########
# soup.find(class_="logo-info")
# soup.find_all(attrs={"data-foo": "value"})
# soup.find_all("a", class_="sister")
# soup.select("a.sister")
# soup.find_all(string="Compte")


# ajouter la taille de l'image à la fin du lien
def addTailleImage(strLinkImg):
    taille_png = str(350)
    return f"-{taille_png}x{taille_png}.png".join(strLinkImg.split('.png'))


# recupère pour chaque produit, le prix, stock
def infoParProduit(link):
    name, price, stock, pic = 0, 0, 0, 0
    pageProduit = requests.get(link)
    soupP = BeautifulSoup(pageProduit.content, 'lxml')

    # name = <h1 class="product_title entry-title">Bulbasaur</h1>
    name = soupP.find_all('h1', class_="product_title entry-title")[0].string

    # price = <span class="woocommerce-Price-amount amount"><span class="woocommerce-Price-currencySymbol">£</span>63.00</span>
    devise = soupP.find_all('span', class_="woocommerce-Price-currencySymbol")[0].string
    price = str(soupP.find_all('span', class_="woocommerce-Price-amount")[1]).split(devise)[1].split('</span>')[1]
    price += devise

    # stock = <p class="stock in-stock">45 in stock</p>
    stock = soupP.find_all('p', class_="stock in-stock")[0].string
    stock = stock.split(" ")
    stock = stock[0]

    # pics <img role="presentation" alt="" src="https://scrapeme.live/wp-content/uploads/2018/08/001.png" ...
    pic = soupP.find_all('img')[0].get('src')
    pic = addTailleImage(pic)

    return name, price, stock, pic


# links <a ... class="woocommerce-LoopProduct-link woocommerce-loop-product__link"
links = []
for link in soup.find_all('a', class_="woocommerce-LoopProduct-link woocommerce-loop-product__link"):
    links.append(link.get('href'))


# names & prices & stocks & pics
names = []
prices = []
stocks = []
pics = []

for i in links:
    name, price, stock, pic = infoParProduit(i)
    names.append(name)
    prices.append(price)
    stocks.append(stock)
    pics.append(pic)

# verification
print(len(links))
print(len(names))
print(len(prices))
print(len(stocks))
print(len(pics))


########## DONNÉES EN DATAFRAME ##########


df = pd.DataFrame({
    'Name': names,
    'Price': prices,
    'Stock': stocks,
    'Url': links,
    'Images': pics
}, range(1,len(links)+1))


# chargement dans un fichier csv
#os.getcwd()
#os.chdir("Documents/python/extraction_web/Pokemon")

df.to_csv('Documents/python/extraction_web/Pokemon/products.csv', index=False, encoding='utf-8')


########## AVEC SELECTORLIB PLUS RAPIDE ##########


# url
url1 = 'https://scrapeme.live/shop/'


# chargement de la page
r1 = requests.get(url1)


# architecture des données scrappées
e1 = Extractor.from_yaml_string("""
product:
    css: li.product
    xpath: null
    multiple: true
    type: Text
    children:
        name:
            css: h2.woocommerce-loop-product__title
            xpath: null
            type: Text
        price:
            css: span.woocommerce-Price-amount
            xpath: null
            type: Text
        link:
            css: a.woocommerce-LoopProduct-link
            xpath: null
            type: Link
        image:
            css: img.attachment-woocommerce_thumbnail
            xpath: null
            type: Image
    """)


# dictionnaire contenant nos données
e1.extract(r1.text)


N, P, L, I= [], [], [], []
for elem in e1.extract(r1.text)['product']:
    N.append(elem['name'])
    P.append(elem['price'])
    L.append(elem['link'])
    I.append(elem['image'])


# verification
print(len(L))
print(len(N))
print(len(P))
print(len(I))


# DONNÉES EN DATAFRAME


df1 = pd.DataFrame({
    'Name': N,
    'Price': P,
    'Url': L,
    'Images': I
}, range(1,len(L)+1))

