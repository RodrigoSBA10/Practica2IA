# search.py
# ---------
# Algoritmos genéricos de búsqueda (sin typing):
# DFS, BFS, UCS, A*

import util


class SearchProblem:
    """
    Interfaz mínima que debe implementar un problema de búsqueda.
    """
    def getStartState(self):
        raise NotImplementedError

    def isGoalState(self, state):
        raise NotImplementedError

    def getSuccessors(self, state):
        """
        Debe regresar lista de triples:
          (successor_state, action, stepCost)
        """
        raise NotImplementedError

    def getCostOfActions(self, actions):
        raise NotImplementedError

#DFS con nodos 
def depthFirstSearch(problem):
    """
    DFS: usa Stack (LIFO). No garantiza optimalidad.
    Graph Search: usa visitados para evitar ciclos.
    """
    frontera = util.Stack()
    visitados = set()
    nodos_generados = 0
    nodos_expandidos = 0

    inicio = problem.getStartState()
    frontera.push((inicio, []))  # (estado, camino)
    #Aumentar los nodos expandidos al realizar pop
    nodos_expandidos += 1


    while not frontera.isEmpty():
        estado, camino = frontera.pop()

        if problem.isGoalState(estado):
            print("Nodos genrados son: ", nodos_generados, "Nodos expandidos: ",nodos_expandidos)
            return camino

        if estado in visitados:
            continue
        visitados.add(estado)

        for sucesor, accion, costo in problem.getSuccessors(estado):
            if sucesor not in visitados:
                frontera.push((sucesor, camino + [accion]))
                nodos_generados += 1


    return [], nodos_generados, nodos_expandidos
"""
    implementacion con DFS usando, un arbol sin visitados  
"""
def sin_visitados_dfs(problem):
    frontera = util.Stack()
    inicio = problem.getStartState()
    frontera.push((inicio, []))
    nodos_generados = 0
    nodos_expandidos = 0

    while not frontera.isEmpty():
        estado, camino = frontera.pop()
        nodos_expandidos += 1
        if problem.isGoalState(estado):
            print("Nodos genrados son: ", nodos_generados, "Nodos expandidos: ",nodos_expandidos)
            return camino
        for sucesor, accion, costo in problem.getSuccessors(estado):
            frontera.push((sucesor, camino + [accion]))
            nodos_generados += 1
   
    return [], nodos_generados, nodos_expandidos



def breadthFirstSearch(problem):
    """
    BFS: usa Queue (FIFO). Encuentra menos pasos si costos uniformes.
    Marcamos visitado al ENCOLAR para evitar duplicados.
    """
    frontera = util.Queue()
    visitados = set()

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    frontera.push((inicio, []))
    visitados.add(inicio)

    while not frontera.isEmpty():
        estado, camino = frontera.pop()

        if problem.isGoalState(estado):
            return camino

        for sucesor, accion, costo in problem.getSuccessors(estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.push((sucesor, camino + [accion]))

    return []


def uniformCostSearch(problem):
    """
    UCS: usa PriorityQueue por costo acumulado g(n).
    Optimalidad si costos no negativos.
    """
    frontera = util.PriorityQueue()
    best_g = {}  # estado -> mejor costo encontrado

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    frontera.push((inicio, [], 0), 0)
    best_g[inicio] = 0

    while not frontera.isEmpty():
        estado, camino, g = frontera.pop()

        if g > best_g.get(estado, float("inf")):
            continue

        if problem.isGoalState(estado):
            return camino

        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            nuevo_g = g + step_cost
            if nuevo_g < best_g.get(sucesor, float("inf")):
                best_g[sucesor] = nuevo_g
                frontera.push((sucesor, camino + [accion], nuevo_g), nuevo_g)

    return []


def nullHeuristic(state, problem=None):
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*: usa PriorityQueue con f(n) = g(n) + h(n).
    Optimalidad si h es admisible (y consistente).
    """
    frontera = util.PriorityQueue()
    best_g = {}

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    g0 = 0
    f0 = g0 + heuristic(inicio, problem)
    frontera.push((inicio, [], g0), f0)
    best_g[inicio] = g0

    while not frontera.isEmpty():
        estado, camino, g = frontera.pop()

        if g > best_g.get(estado, float("inf")):
            continue

        if problem.isGoalState(estado):
            return camino

        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            nuevo_g = g + step_cost
            if nuevo_g < best_g.get(sucesor, float("inf")):
                best_g[sucesor] = nuevo_g
                nuevo_f = nuevo_g + heuristic(sucesor, problem)
                frontera.push((sucesor, camino + [accion], nuevo_g), nuevo_f)

    return []


# Alias
dfs = depthFirstSearch
dfs_sin = sin_visitados_dfs
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch