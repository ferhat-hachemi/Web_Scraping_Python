import requests
from bs4 import BeautifulSoup

# liens et construction de graphe

# liste des liens d'une page wiki
# renvoie la liste des liens ou pointe une page wiki
def liste_liens(page):
    url = 'https://iceandfire.fandom.com/wiki/'
    urlSource = url + page
    links_list = []
    try:
        response = requests.get(urlSource) 
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find("div", class_="mw-parser-output")
        a = result.find_all('a')
        for elt in a:
            link = elt.get('href')
            if link.startswith('/wiki/') and "#" not in link and ":" not in link: # on ne recupere pas les images
                    title = link[6::] # on recupere juste ce qu'il y a apres /wiki/
                    if title not in links_list:
                        links_list.append(title)
        return links_list

    # pour gerer les erreurs de requete ou de connexion...
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

# sauvegarde de dictionnaire dans un fichier
def svg_dico(dico, fichier):
    file = open(fichier, "w")
    for item in dico.items():
        file.write(item[0] + ':')
        file.write(str(item[1]) + '\n')
    file.close()

# charger un fichier dans un dictionnaire
def chg_dico(fichier):
    dico = {}
    with open(fichier, "r") as file:
        for line in file:
            cle, valeur = line.split(":")
            dico[cle] = eval(valeur) # la fonction eval pour recuperer la valeur de type liste
        file.close()
        return dico

# parcours en largeur de graphe
def parcours_largeur(source):
    dico = {}
    file = [source]
    visited = [source]
    dico[source] = liste_liens(source)
    while file: # tant que la file n'est pas vide on continue a visiter les noeuds
        sommet = file.pop(0) 
        for voisin in liste_liens(sommet):
            if voisin not in visited:
                dico[voisin] = liste_liens(voisin)
                file.append(voisin)
                visited.append(voisin)
                svg_dico(dico,"parcours_largeur_wiki.txt")




