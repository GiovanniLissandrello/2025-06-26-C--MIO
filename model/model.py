import copy
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def buildGraph(self, anno1, anno2):

        nodi = DAO.getAllConstructors()
        self._graph.add_nodes_from(nodi)
        for nodi in nodi:
            self._idMap[nodi.constructorId] = nodi

        archi = DAO.getAllArchi(anno1, anno2, self._idMap)

        for arco in archi:
            self._graph.add_edge(arco.u, arco.v, weight = arco.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges(data=True))

    def fillPosizionamenti(self,anno1,anno2):
        nodi = self._graph.nodes()
        for n in nodi:
            #lista di tuple, nella posizione 1 l'anno, nella posizione 2 l'oggetto Posizione (driverid, posizione)
            lista_posizionamenti = DAO.getAllPosizionamenti(anno1,anno2,n.constructorId)
            n.dizionario_posizioni = defaultdict(list)
            for anno, oggetto in lista_posizionamenti:
                n.dizionario_posizioni[anno].append(oggetto)


    def getConnessa(self):

        componente_massima = max(list(nx.connected_components(self._graph)), key = len)
        lista_punteggi = []
        for n in componente_massima:
            vicini = list(self._graph.neighbors(n))
            best_peso = 0
            for v in vicini:
                if self._graph[n][v]["weight"] > best_peso:
                    best_peso = self._graph[n][v]["weight"]

            lista_punteggi.append((n,best_peso))

        lista_punteggi.sort(key = lambda x:x[1], reverse = True)

        return lista_punteggi

    def getYears(self):
        return DAO.getAllYears()

    def getNodes(self):
        return list(self._graph.nodes())

    def fillIndiceSfortuna(self,anno1,anno2,M):
        componente_massima = max(list(nx.connected_components(self._graph)), key=len)
        lista_info_campionati = DAO.getNumCampionati(anno1, anno2, M, self._idMap)
        # lista_info_campionatiè la lista dei costruttori che rispettano le condizioni iniziali (M campionati e range selezionato)
        self.lista_validi = []
        for n in componente_massima:
            if n in lista_info_campionati:
                self.lista_validi.append(n)

        # lista_validi rappresenta la lista dei nodi appartenenti alla componente connessa che rispettano le condizioni

        for v in self.lista_validi:
            numero_gare_completate = DAO.getNumGareCompletate(anno1, anno2, v.constructorId)[0]
            np = 0
            for lista in v.dizionario_posizioni.values():
                np += len(lista)

            v.indice_sfortuna = 1 - (numero_gare_completate / np)


    def getPath(self,k):

        self._bestPath = []
        self._bestscore = 0
        parziale = []

        if k > len(self.lista_validi):
            return [],0

        for n in self.lista_validi:
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,k)
                parziale.pop()

        return self._bestPath, self._bestscore

    def _ricorsione(self,parziale,k):

        #condizione di ottimalità
        if len(parziale) == k:
            score = 0
            for n in parziale:
                score += n.indice_sfortuna

            if score > self._bestscore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestscore = score

            return
        #condizione di terminazione
        if (len(self.lista_validi) - len(parziale)) < (k-len(parziale)):
            return

        for n in self.lista_validi:
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,k)
                parziale.pop()




 #condizione di ricorsione
        # lista_vicini = list(self._graph.neighbors(parziale[-1]))
        # lista_vicini_validi = []
        # for v in lista_vicini:
        #     if v in self.lista_validi:
        #         lista_vicini_validi.append(v)
        #
        # lista_vicini_validi.sort(key = lambda x: x.indice_sfortuna, reverse = True)