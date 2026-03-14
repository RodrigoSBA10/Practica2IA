# search.py
# ---------
# Algoritmos genéricos de búsqueda (sin typing):
# DFS, BFS, UCS, A*, DLS, IDDFS
# Incluye variantes: grafo (con visitados), árbol (sin visitados),
# e instrumentadas (con contadores nodos_generados / nodos_expandidos).

import util


class SearchProblem:
    """
    Interfaz mínima que debe implementar un problema de búsqueda.
    """
# ESTADO INICIAL
    def getStartState(self):
        raise NotImplementedError

# ESTADO FINAL
    def isGoalState(self, state):
        raise NotImplementedError
# SUCESORES
    def getSuccessors(self, state):
        """
        Debe regresar lista de triples:
          (successor_state, action, stepCost)
        """
        raise NotImplementedError
# COSTO DE LAS ACCIONES, CAMINO = LISTA DE ESTADOS
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
    


    while not frontera.isEmpty():
        estado, camino = frontera.pop()
        #Aumentar los nodos expandidos al realizar pop
        nodos_expandidos += 1

        if problem.isGoalState(estado):
            return camino, nodos_generados, nodos_expandidos

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
            return camino, nodos_generados, nodos_expandidos
        for sucesor, accion, costo in problem.getSuccessors(estado):
            frontera.push((sucesor, camino + [accion]))
            nodos_generados += 1
   
    return [], nodos_generados, nodos_expandidos


def breadthFirstSearch(problem):
    """
    BFS grafo: usa Queue (FIFO). Marca visitado al encolar.
    Garantiza camino de menor número de pasos (costos uniformes).
    """
    frontera = util.Queue()
    visitados = set()
    nodos_generados = 0
    nodos_expandidos = 0 

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    frontera.push((inicio, []))
    visitados.add(inicio)

    while not frontera.isEmpty():
        estado, camino = frontera.pop()
        nodos_expandidos += 1

        if problem.isGoalState(estado):
            return camino, nodos_generados, nodos_expandidos

        for sucesor, accion, costo in problem.getSuccessors(estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.push((sucesor, camino + [accion]))
                nodos_generados += 1

    return [],nodos_generados, nodos_expandidos

# ===========================================================================
# DFS — Búsqueda en Profundidad
# ===========================================================================

# BFS grafo con contadores
# Retornamos(acciones, nodos_generados, nodos_expandidos, termino).
def breadthFirstSearchStats(problem, max_iter=100000):
    """
    BFS grafo con contadores.
    Retorna (acciones, nodos_generados, nodos_expandidos, termino).
    """
    frontera = util.Queue()
    visitados = set()
    nodos_generados = 0
    nodos_expandidos = 0

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return [], 0, 0, True

    frontera.push((inicio, []))
    visitados.add(inicio)
    nodos_generados += 1

    iters = 0
    while not frontera.isEmpty() and iters < max_iter:
        estado, camino = frontera.pop()
        nodos_expandidos += 1
        iters += 1

        if problem.isGoalState(estado):
            return camino, nodos_generados, nodos_expandidos, True

        for sucesor, accion, costo in problem.getSuccessors(estado):
            if sucesor not in visitados:
                visitados.add(sucesor)
                frontera.push((sucesor, camino + [accion]))
                nodos_generados += 1

    return [], nodos_generados, nodos_expandidos, False


# BFS árbol sin visitados
# Retormos (acciones, nodos_generados, nodos_expandidos, termino)
def breadthFirstSearchTree(problem, max_iter=10000):
    """
    BFS árbol (sin visitados). Puede ciclar en grafos con ciclos.
    Retorna (acciones, nodos_generados, nodos_expandidos, termino).
    """
    frontera = util.Queue()
    nodos_generados = 0
    nodos_expandidos = 0

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return [], 0, 0, True

    frontera.push((inicio, []))
    nodos_generados += 1

    iters = 0
    while not frontera.isEmpty() and iters < max_iter:
        estado, camino = frontera.pop()
        nodos_expandidos += 1
        iters += 1

        if problem.isGoalState(estado):
            return camino, nodos_generados, nodos_expandidos, True

        for sucesor, accion, costo in problem.getSuccessors(estado):
            frontera.push((sucesor, camino + [accion]))
            nodos_generados += 1

    return None, nodos_generados, nodos_expandidos, False


# ===========================================================================
# UCS — Búsqueda de Costo Uniforme
# ===========================================================================

def uniformCostSearch(problem):
    """
    UCS: usa PriorityQueue por costo acumulado g(n).
    Óptimo si costos no negativos.
    """
    frontera = util.PriorityQueue()
    best_g = {}

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


def uniformCostSearchStats(problem):
    """
    UCS con contadores.
    Retorna (acciones, nodos_generados, nodos_expandidos, termino).
    """
    frontera = util.PriorityQueue()
    best_g = {}
    nodos_generados = 0
    nodos_expandidos = 0

    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return [], 0, 0, True

    frontera.push((inicio, [], 0), 0)
    best_g[inicio] = 0
    nodos_generados += 1

    while not frontera.isEmpty():
        estado, camino, g = frontera.pop()

        if g > best_g.get(estado, float("inf")):
            continue

        nodos_expandidos += 1

        if problem.isGoalState(estado):
            return camino, nodos_generados, nodos_expandidos

        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            nuevo_g = g + step_cost
            if nuevo_g < best_g.get(sucesor, float("inf")):
                best_g[sucesor] = nuevo_g
                frontera.push((sucesor, camino + [accion], nuevo_g), nuevo_g)
                nodos_generados += 1

    return [], nodos_generados, nodos_expandidos


# ===========================================================================
# A* — Búsqueda A Estrella
# ===========================================================================

def nullHeuristic(state, problem=None):
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*: usa PriorityQueue con f(n) = g(n) + h(n).
    Óptimo si h es admisible (y consistente).
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


# ===========================================================================
# DLS — Depth-Limited Search (búsqueda en profundidad con límite)
# ===========================================================================

def depthLimitedSearch(problem, limit):
    """
    DFS con límite de profundidad.
    Usa path-checking para evitar ciclos dentro del mismo camino.

    Devuelve:
        lista de acciones si encuentra la meta dentro del límite
        None si no encuentra solución dentro del límite
    """
    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    # Pila: (estado, camino, profundidad, ruta_actual)
    # ruta_actual = frozenset de estados en el camino actual (path checking)
    frontera = util.Stack()
    frontera.push((inicio, [], 0, frozenset([inicio])))

    while not frontera.isEmpty():
        estado, camino, prof, ruta = frontera.pop()

        if problem.isGoalState(estado):
            return camino

        if prof < limit:
            for sucesor, accion, costo in problem.getSuccessors(estado):
                if sucesor not in ruta:
                    frontera.push((sucesor, camino + [accion], prof + 1, ruta | {sucesor}))

    return None


def depthLimitedSearchStats(problem, limit):
    """
    DLS con contadores.
    Retorna (acciones_o_None, nodos_generados, nodos_expandidos).
    """
    inicio = problem.getStartState()
    nodos_generados = 1
    nodos_expandidos = 0

    if problem.isGoalState(inicio):
        return [], nodos_generados, nodos_expandidos

    frontera = util.Stack()
    frontera.push((inicio, [], 0, frozenset([inicio])))

    while not frontera.isEmpty():
        estado, camino, prof, ruta = frontera.pop()
        nodos_expandidos += 1

        if problem.isGoalState(estado):
            return camino, nodos_generados, nodos_expandidos

        if prof < limit:
            for sucesor, accion, costo in problem.getSuccessors(estado):
                if sucesor not in ruta:
                    frontera.push((sucesor, camino + [accion], prof + 1, ruta | {sucesor}))
                    nodos_generados += 1

    return None, nodos_generados, nodos_expandidos


# ===========================================================================
# IDDFS — Iterative Deepening Depth-First Search
# ===========================================================================

def iterativeDeepeningSearch(problem, max_depth=50):
    """
    Búsqueda en profundidad iterativa (IDDFS).
    Ejecuta DLS con límites 0, 1, 2, ..., max_depth.
    Combina la completitud de BFS con el bajo uso de memoria de DFS.
    """
    for limit in range(max_depth + 1):
        result = depthLimitedSearch(problem, limit)
        if result is not None:
            return result
    return []


def iterativeDeepeningSearchStats(problem, max_depth=50):
    """
    IDDFS con contadores acumulados de todas las iteraciones.
    Retorna (acciones, nodos_generados_total, nodos_expandidos_total, termino).
    """
    total_gen = 0
    total_exp = 0

    for limit in range(max_depth + 1):
        result, gen, exp = depthLimitedSearchStats(problem, limit)
        total_gen += gen
        total_exp += exp
        if result is not None:
            return result, total_gen, total_exp#, True

    return [], total_gen, total_exp#, False


# ===========================================================================
# DLS sin path-checking (para experimento: ¿qué pasa sin control de ciclos?)
# ===========================================================================

def depthLimitedSearchNoCycleCheck(problem, limit):
    """
    DLS sin path-checking. Puede expandir estados repetidos en el mismo camino.
    """
    inicio = problem.getStartState()
    if problem.isGoalState(inicio):
        return []

    frontera = util.Stack()
    frontera.push((inicio, [], 0))

    while not frontera.isEmpty():
        estado, camino, prof = frontera.pop()

        if problem.isGoalState(estado):
            return camino

        if prof < limit:
            for sucesor, accion, costo in problem.getSuccessors(estado):
                frontera.push((sucesor, camino + [accion], prof + 1))

    return None


def iterativeDeepeningSearchNoCycleCheck(problem, max_depth=50):
    """
    IDDFS sin path-checking.
    """
    for limit in range(max_depth + 1):
        result = depthLimitedSearchNoCycleCheck(problem, limit)
        if result is not None:
            return result
    return []


# ===========================================================================
# Alias para compatibilidad
# ===========================================================================
dfs = depthFirstSearch
dfs_sin = sin_visitados_dfs
bfs = breadthFirstSearch
#ucs = uniformCostSearch
ucs = uniformCostSearchStats
astar = aStarSearch
dls = depthLimitedSearch
#iddfs = iterativeDeepeningSearch
iddfs = iterativeDeepeningSearchStats