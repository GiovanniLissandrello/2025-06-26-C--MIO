import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._anno1 = None
        self._anno2 = None

    def fillddYear1(self):

        lista_anni = self._model.getYears()
        for anno in lista_anni:
            self._view._ddYear1.options.append(
                ft.dropdown.Option(data=anno,
                                   key=anno,
                                   text=anno,
                                   on_click=self.read_anno1)
            )

    def read_anno1(self, e):
        if e.control.data is None:
            self._anno1 = None
        else:
            self._anno1 = e.control.data

    def fillddYear2(self):

        lista_anni = self._model.getYears()
        for anno in lista_anni:
            self._view._ddYear2.options.append(
                ft.dropdown.Option(data=anno,
                                   key=anno,
                                   text=anno,
                                   on_click=self.read_anno2)
            )

    def read_anno2(self, e):
        if e.control.data is None:
            self._anno2 = None
        else:
            self._anno2 = e.control.data

    def handleBuildGraph(self, e):

        if self._anno1 is None or self._anno2 is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text(f"Inserisci tutti i campi"))

        self._model.buildGraph(self._anno1,self._anno2)
        n, m = self._model.getGraphDetails()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato! Il grafo è costituito di {n} nodi ed {m} archi"))

        self._view.update_page()

    def handlePrintDetails(self, e):

        lista_punteggi = self._model.getConnessa()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Componenete connessa più grande: "))

        for elemento in lista_punteggi:
            self._view._txt_result.controls.append(
                ft.Text(f" {elemento[0].name} --- {elemento[1]}"))

        self._view.update_page()

    def handleCercaTeamSfortunati(self, e):

        k = int(self._view._txtInSoglia.value)
        M = int(self._view._txtInNumDiEdizioni.value)
        self._view._txt_result.controls.clear()
        if k is None or M is None:
            self._view._txt_result.controls.append(
                ft.Text(f"Inserisci tutti i campi"))

        if k<0 or M<0:
            self._view._txt_result.controls.append(
                ft.Text(f"Inserisci valori positivi"))

        self._model.fillPosizionamenti(self._anno1,self._anno2)
        self._model.fillIndiceSfortuna(self._anno1,self._anno2,M)
        best_percorso , score = self._model.getPath(k)

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"L'indice di sfortuna massima è : {score}"))
        self._view._txt_result.controls.append(
            ft.Text(f"I costruttori più sfortunati: "))
        for b in best_percorso:
            self._view._txt_result.controls.append(
                ft.Text(f"{b.name}"))

        self._view.update_page()