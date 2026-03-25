class OchoPuzzle:
    #Constructor
    def __init__(self, start):
        self.start = start
        self.meta = (1,2,3,4,5,6,7,8,0)

    #Estado inicial del problema
    def getStartState(self):
        return self.start

    # Metodo para validar si se llego a la meta
    def isGoalState(self, state):
        return state == self.meta

    # Genera los sucesres validos, cada sucesor es un tupla (nuevo_estado, accion, costo)
    def getSuccessors(self, state):
        sucesores = []
        # Lista mas facil de manipular
        lista = list(state)
        vacio = lista.index(0)
        fila = vacio // 3
        col = vacio % 3
        movimientos = []
        if fila > 0:
            movimientos.append((-1, 0, "Mov. Arriba"))
        if fila < 2:
            movimientos.append((1,0,"Mov. Abajo"))
        if col > 0:
            movimientos.append((0,-1, "Mov. Izquierda"))
        if col < 2:
            movimientos.append((0, 1, "Mov. Derecha"))
        for mf, mc, accion in movimientos:
            nf = fila + mf
            nc = col + mc
            nuevo_vacio = (nf * 3) + nc
            nueva_lista = lista.copy()
            nueva_lista[vacio], nueva_lista[nuevo_vacio] = nueva_lista[nuevo_vacio], nueva_lista[vacio]
            costo = 1
            nuevo_estado = tuple(nueva_lista)
            sucesores.append((nuevo_estado, accion, costo))
        return sucesores

    def getCostOfActions(self, actions):
        costo = 0
        for acciones in actions:
            costo += 1
        return  costo