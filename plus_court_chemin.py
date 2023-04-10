# partie du plus court chemin entre deux pages

# le plus court chemin entre deux pages wiki (source et cible)
def plus_court_chemin(graph,source, cible):
    if source == cible:
        return [source]
   
    visited = []
    file = [[source]]
    while file:
        chemin = file.pop(0)
        sommet = chemin[-1] # on prend le dernier noeud du chemin
        if sommet not in visited:
            voisins = graph[sommet]
            for voisin in voisins: 
                nouveau_chemin = list(chemin)
                nouveau_chemin.append(voisin)
                file.append(nouveau_chemin)
                if voisin == cible: 
                    return nouveau_chemin
            visited.append(sommet)
    return None

# calcule le nombre de caracteres d'une page
def nombre_caracteres(cible):
     return len(cible)

# calcule le nombre de voyelles d'une page
def nombre_voyelle(cible):
    nb = 0
    list_voyelle = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y']
    for v in list_voyelle:
        nb = nb + cible.count(v)
    return nb

# le poids total d'une page
def cout_chemin(cible):
    return nombre_caracteres(cible) + nombre_voyelle(cible)

# algorithme Dijkstra (plus court chemin avec un cout minimum)
def pcc_voyelles(graph,source,cible):
    distance_min = {}
    predecessor = {}
    nonVisited = graph
    infinity = 999999
    chemin = []
    for sommet in nonVisited: # initialise tous les sommets a infini sauf le sommet
        distance_min[sommet] = infinity
    distance_min[source] = 0

    while nonVisited:
        min = None
        for sommet in nonVisited:
            if min is None:
                min = sommet
            elif distance_min[sommet] < distance_min[min]:
                min = sommet
        chemin1 = graph[min]
        for voisin in chemin1:
            if cout_chemin(voisin) + distance_min[min] < distance_min[voisin]: # on met a jour les distances 
                distance_min[voisin] = cout_chemin(voisin) + distance_min[min]
                predecessor[voisin] = min
        nonVisited.pop(min)
    current  = cible
    while current != source:
         try:
            chemin.insert(0,current)
            current = predecessor[current]
         except KeyError:
            return None
    chemin.insert(0,source)

    if distance_min[cible] != infinity:
        print(f"le cout total est {int(distance_min[cible] + cout_chemin(source))}")
    return chemin
