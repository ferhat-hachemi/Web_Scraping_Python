import requests
from bs4 import BeautifulSoup
import liens_et_graphe as lg

# Inceste et descendance

# pour retrouver l'url d'une page apres l'envoie de requete 
# 
def get_url(page):
    lien = 'https://iceandfire.fandom.com/wiki/'
    url = lien + page
    response = requests.get(url)
    link = response.url[len(lien)::]
    return link

# pour recuperer la section family de chaque personnage dans le wiki
def relation_family(page):
    relation_liste = []
    url = 'https://iceandfire.fandom.com/wiki/' + page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find_all("section", class_="pi-item pi-group pi-border-color pi-collapse pi-collapse-open") # on detecte d'abord la section => h2.text = "Family" 
    for section in result:
        if section.h2.text == "Family":
            all_h3 = section.find_all('h3')
            for h3 in all_h3: # ensuite chaque type de relation est presente avec un h3
                if h3.text == "Father" or h3.text == "Mother" or h3.text == "Children" or h3.text == "Lover" or h3.text == "Spouse" or h3.text == "Siblings":
                    div = h3.find_next("div") # les liens a (membres de familles) sont dans la div qui suit ce h3
                    a = div.find_all('a')
                    for lien in a:
                        link = lien.get('href')
                        
                        if link.startswith('/wiki/'):
                            page_link = link[6::]
                            if lien.get('class') == ['mw-redirect']: 
                                link = get_url(page_link) # on recupere le vrai lien de la page pour avoir un nom valable pour la suite
                                relation_liste.append([link,h3.text])

                            else: 
                                relation_liste.append([page_link,h3.text])
            return relation_liste

# representation de graphe des personnages dans un fichier
def graphe_personnage():
    dico = lg.chg_dico("parcours_largeur_wiki.txt")
    dico_family = {}
    for key in dico.keys():
        page = get_url(key)
        if relation_family(page) and page not in dico_family.keys(): # on elimine les pages qui se repete avec un nom different pour construire le graphe
            dico_family[page] = relation_family(key)
            lg.svg_dico(dico_family,"graphe_personnage.txt")
                    
# liste des couple incestueux
# on separe les relations en deux listes et si un "personnage" est present dans les deux donc on a un couple (key,personnage)
def couple_incestueux():
    couple = []
    dico = lg.chg_dico("graphe_personnage.txt")
    for key in dico.keys():
        list_love = []
        list_family = []
        for elt in dico[key]:
            if elt[1] == "Spouse" or elt[1] == "Lover":
                list_love.append(elt[0])
            else:
                list_family.append(elt[0])
    
            for element in list_family:
                if element in list_love and [element,key] not in couple and [key, element] not in couple:
                    couple.append([key, element])
    print(len(couple))
    return couple

# graphe de descendance (parent, grand-parent...)
# une cle dans le graphe c'est l'ancetre de tous les elements de la liste
def graphe_ancetre_descendant():
    dico_ancetre = {}
    dico = lg.chg_dico("graphe_personnage.txt")
    for key in dico.keys():
        descendants = []
        children = []
        for elt in dico[key]:
            if elt[1] == "Children":
                children.append(elt[0]) # on visite d'abord la premiere descendance
        while children: # tant qu'on en a des fils des fils... on continue a les visiter 
            fils = children.pop()
            if fils not in descendants:
                descendants.append(fils)
                if fils in dico.keys():
                    for fils2 in dico[fils]:
                        if fils2[1] == "Children":
                            children.append(fils2[0])
        if descendants:
            dico_ancetre[key] = descendants
            lg.svg_dico(dico_ancetre, "graphe_ancetre_descendant.txt")

