# search.py
# ---------
# Algoritmos genéricos de búsqueda (sin typing):
# DFS, BFS, UCS, A*, DLS, IDDFS
# Incluye variantes: grafo (con visitados), árbol (sin visitados),
# e instrumentadas (con contadores nodos_generados / nodos_expandidos).
import math
import time

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


# ===========================================================================
# BFS — Búsqueda en Anchura
# ===========================================================================


def breadthFirstSearch(problem):
    """
    BFS grafo: usa Queue (FIFO). Marca visitado al encolar.
    Garantiza camino de menor número de pasos (costos uniformes).
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

# ===========================================================================
# DFS — Búsqueda en Profundidad
# ===========================================================================

def depthFirstSearch(problem):
    """
    DFS grafo: usa Stack (LIFO). Usa visitados para evitar ciclos.
    No garantiza optimalidad.
    """
    frontera = util.Stack()
    visitados = set()

    inicio = problem.getStartState()
    frontera.push((inicio, []))

    while not frontera.isEmpty():
        estado, camino = frontera.pop()

        if problem.isGoalState(estado):
            return camino

        if estado in visitados:
            continue
        visitados.add(estado)

        for sucesor, accion, costo in problem.getSuccessors(estado):
            if sucesor not in visitados:
                frontera.push((sucesor, camino + [accion]))

    return []


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
    expandidos = 0
    generados = 0

    inicio = problem.getStartState()
    inicio_tiempo = time.time()

    if problem.isGoalState(inicio):
        return []

    # Insertar: (estado, camino, costo_acumulado), prioridad = g
    frontera.push((inicio, [], 0), 0)
    best_g[inicio] = 0

    while not frontera.isEmpty():
        estado, camino, g = frontera.pop()

        if g > best_g.get(estado, float("inf")):
            continue

        expandidos += 1

        if problem.isGoalState(estado):
            tiempo_total = time.time() - inicio_tiempo
            return {
                "Camino": camino,
                "Costo": g,
                "Expandidos": expandidos,
                "Generados": generados,
                "Tiempo": tiempo_total,
            }

        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            generados += 1
            nuevo_g = g + step_cost
            if nuevo_g < best_g.get(sucesor, float("inf")):
                best_g[sucesor] = nuevo_g
                frontera.push((sucesor, camino + [accion], nuevo_g), nuevo_g)

    return None

def uniformCostSearchStats(problem):
    """
    UCS con contadores.
    Retorna (acciones, nodos_generados, nodos_expandidos, termino).
    """
    # cola de prioridad
    frontera = util.PriorityQueue()
    # GUarda el mejor costo conocido
    best_g = {}
    nodos_generados = 0
    nodos_expandidos = 0
    # Estado iniciol del problema
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
            print("UCS nodos expandidos: ", nodos_expandidos, " Nodos generados: ", nodos_generados)
            return camino, nodos_generados, nodos_expandidos, True

        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            nuevo_g = g + step_cost
            if nuevo_g < best_g.get(sucesor, float("inf")):
                best_g[sucesor] = nuevo_g
                frontera.push((sucesor, camino + [accion], nuevo_g), nuevo_g)
                nodos_generados += 1

    return [], nodos_generados, nodos_expandidos, False


# ===========================================================================
# A* — Búsqueda A Estrella
# ===========================================================================
#Heuristica null
def nullHeuristic(state, problem=None):
    return 0

#Heuristica para el problema 8Puzle
def heuristicaFueraLugar(state, problem=None):
    fueraLugar = 0
    #Con enumerate da la iteracion del for con el valor de la pos y el valor que esta en esa pos
    for i , valor in enumerate(state): #Se itera con la pos con el valor
        if valor != 0:
            if (valor-1) != i: # si esta mal
                fueraLugar += 1 #Se suma uno
    return fueraLugar



def heuriticaManhattan(state, problem=None):
    distancia = 0
    for i, valor in enumerate(state):
        if valor == 0:
            continue
        fila_actual = i // 3
        columna_actual = i % 3
        fila_meta = (valor -1) // 3
        columna_meta = (valor -1 ) % 3
        distancia += abs(fila_actual - fila_meta) + abs(columna_actual - columna_meta)
    return distancia

#Heuristica para el problema de desarrolladores 
def heuristica_desarrolladores(state, problem=None):
    dev_izq, bugs_izq, vehiculo = state
    #Verifica si ya esta en la meta
    if dev_izq == 0 and bugs_izq == 0:
        return 0
    #Costos minimo 
    costo_estimado = (dev_izq * 2) + (bugs_izq * 1)

    if vehiculo == 1:
        costo_estimado += 1
    return costo_estimado



def heuristicaDesarrolladores(state, problem=None):
    dev_izq, bugs_izq, _ = state
    return (2 * dev_izq) + bugs_izq


def heuristicaDesa(state, problem=None):
    
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    frontera = util.PriorityQueue() #Cola de prioridad
    best_g = {} #Guardara el mejor costo
    expandidos = 0
    generados = 0
    #Estado inicial
    inicio = problem.getStartState()
    inicio_tiempo = time.time()
    #Verifica si ya es solucion 
    if problem.isGoalState(inicio):
        return []
    #Costos iniciales 
    g0 = 0
    h0 = heuristic(inicio, problem)
    f0 = g0 + h0

    print("\n=== INICIO A* ===")
    print(f"Estado inicial: {inicio} | g(n): {g0} h(n): {h0} f(n): {f0}\n")
    
    # Insertar en la frontera: (estado, camino, costo)
    frontera.push((inicio, [], g0), f0)
    #Guarda mejor costo del inicio
    best_g[inicio] = g0

    while not frontera.isEmpty():
        # Sacar el estado con menor f(n)
        estado, camino, g = frontera.pop()

        if g > best_g.get(estado, float("inf")):
            continue

        expandidos += 1
        #verificamos si es solucion 
        if problem.isGoalState(estado):
            print(f"Nodos expandidos: {expandidos}")
            print(f"Estado final: {estado} | g(n): {g0} h(n): {h0} f(n): {f0}\n")
            tiempo_total = time.time() - inicio_tiempo
            return {
                "Camino": camino,
                "Costo": g,
                "Expandidos": expandidos,
                "Generados": generados,
                "Tiempo": tiempo_total,
            }
            #return camino
        #Expandir los nodos sucesores
        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            generados += 1
            nuevo_g = g + step_cost
            #Verifica si es un mejor camino
            if nuevo_g < best_g.get(sucesor, float("inf")):
                best_g[sucesor] = nuevo_g
                h = heuristic(sucesor, problem) #Calcula la heuristica 
                f = nuevo_g + h #Realiza la operacion para obtener el mejor conston sumando el real con el predicho
                frontera.push((sucesor, camino + [accion], nuevo_g), f)

    return None

def bestFirstSearch(problem, heuristic=nullHeuristic):
    """
    Greedy Best-First Search modificado para la comparativa.
    Evalúa solo h(n), pero rastrea el costo real g(n) para el reporte final.
    """
    frontera = util.PriorityQueue()
    visitados = set()
    expandidos = 0
    generados = 0

    inicio = problem.getStartState()
    inicio_tiempo = time.time()
    
    if problem.isGoalState(inicio):
        return []

    h0 = heuristic(inicio, problem)
    frontera.push((inicio, [], 0), h0)

    while not frontera.isEmpty():
        estado, camino, g = frontera.pop()

        if estado in visitados:
            continue
        visitados.add(estado)

        expandidos += 1

        if problem.isGoalState(estado):
            tiempo_total = time.time() - inicio_tiempo
            return {
                "Camino": camino,
                "Costo": g, # Costo real acumulado, no el número de pasos
                "Expandidos": expandidos,
                "Generados": generados,
                "Tiempo": tiempo_total,
            }

        for sucesor, accion, step_cost in problem.getSuccessors(estado):
            generados += 1
            if sucesor not in visitados:
                nuevo_g = g + step_cost
                h = heuristic(sucesor, problem) 
                # La prioridad sigue siendo SÓLO la heurística (Greedy)
                frontera.push((sucesor, camino + [accion], nuevo_g), h)

    return None

def imprimir_solucion(problem, acciones):
    estado = problem.getStartState()
    print("\n=== Ejemplo ===")
    print(f"Inicio: {estado}")

    for i, accion in enumerate(acciones, 1):
        for sucesor, acc, _ in problem.getSuccessors(estado):
            if acc == accion:
                print(f"{i:02d}. {accion}")
                print(f"    {estado} → {sucesor}")
                estado = sucesor
                break

    print(f"\nMeta alcanzada: {estado}")

def imprimir_paso_a_paso(problem, acciones):
    """
    Imprime el recorrido estado por estado desde el inicio hasta la meta.
    """
    if not acciones:
        print("No se encontro un camino")
        return

    estado_actual = problem.getStartState()
    print(f"Estado Inicial: {estado_actual}")
    costo_acumulado = 0

    for i, accion in enumerate(acciones, 1):
        for sucesor, acc, costo in problem.getSuccessors(estado_actual):
            if acc == accion:
                costo_acumulado += costo
                print(f"Paso {i:02d} | Accion: {accion} (Costo: {costo})")
                print(f"          {estado_actual} -> {sucesor} | Costo Acumulado: {costo_acumulado}")
                estado_actual = sucesor
                break

    print(f"\nMeta Alcanzada: {estado_actual} con costo final de {costo_acumulado}")

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
            return result, total_gen, total_exp, True

    return [], total_gen, total_exp, False


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
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
bestfs = bestFirstSearch
dls = depthLimitedSearch
iddfs = iterativeDeepeningSearch