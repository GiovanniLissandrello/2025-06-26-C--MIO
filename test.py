from model.model import Model

myModel = Model()
myModel.buildGraph(2010,2016)
myModel.fillPosizionamenti(2010,2016)
nNodes, nEdges = myModel.getGraphDetails()
print(f"Num nodes: {nNodes}, num edges: {nEdges}")

# componente = myModel.getConnessa()
# for c in componente:
#     print(f"{c[0].name}, {c[1]}")

# lista = myModel.getPath(2010,2016, 4)
# for l in lista:
#     print(l.name)

nodi = myModel.getNodes()
myModel.fillIndiceSfortuna(2010,2016,6)
print(nodi[0].indice_sfortuna)

best_percorso, score = myModel.getPath(4)
for b in best_percorso:
    print(b.name)