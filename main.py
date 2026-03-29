# Ejecuta DFS/BFSUCS/A* sobre el problema de las jarras.
from search import dfs, bfs, ucs, astar, bestfs, nullHeuristic, dls, iddfs, heuristica_desarrolladores, imprimir_solucion, heuriticaManhattan, heuristicaFueraLugar, imprimir_paso_a_paso
from problems.jarras import JarrasProblem
from problems.Desarroladores import DesarrolladoresBugsProblem
from problems.OchoPuzzle import OchoPuzzle
# Definición de un problema de grafo simple para probar los algoritmos de búsqueda.
class ProblemaGrafo:
    """
    Grafo:
      A -> B (1), A -> C (2)
      B -> D (5)
      C -> D (1)
    Inicio: A
    Meta: D
    """
    def __init__(self):
        self.inicio = "A"
        self.meta = "D"
        self.grafo = {
            "A": [("B", "A->B", 1), ("C", "A->C", 2)],
            "B": [("D", "B->D", 5)],
            "C": [("D", "C->D", 1)],
            "D": []
        }
        self.costos_accion = {
            "A->B": 1,
            "A->C": 2,
            "B->D": 5,
            "C->D": 1
        }

    def getStartState(self):
        return self.inicio

    def isGoalState(self, state):
        return state == self.meta

    def getSuccessors(self, state):
        return self.grafo[state]

    def getCostOfActions(self, actions):
        total = 0
        for a in actions:
            total += self.costos_accion[a]
        return total


# Probamos los algoritmos de búsqueda sobre el grafo definido.
#def main():
#    problema = ProblemaGrafo()

#    sol_dfs = dfs(problema)
#    sol_bfs = bfs(problema)
#    sol_ucs = ucs(problema)
#    sol_astar = astar(problema, heuristic=nullHeuristic)

#    print("DFS :", sol_dfs, " costo:", problema.getCostOfActions(sol_dfs) if sol_dfs else 0)
#    print("BFS :", sol_bfs, " costo:", problema.getCostOfActions(sol_bfs) if sol_bfs else 0)
#    print("UCS :", sol_ucs, " costo:", problema.getCostOfActions(sol_ucs) if sol_ucs else 0)
#    print("A*  :", sol_astar, " costo:", problema.getCostOfActions(sol_astar) if sol_astar else 0)



# Probamos con el problema de las jarras.
def main():
    # Ejemplo clásico: jarra A de 5L, jarra B de 3L, meta (2,0)
    #problema = JarrasProblem(capA=5, capB=3, start=(0, 0), goal=(2, 0))
    problema = DesarrolladoresBugsProblem()
    #problema = OchoPuzzle((1,3,4,2,5,6,7,0,8))
    #astarM = astar(problema, heuristic=heuriticaManhattan)
    #bestM = bestfs(problema, heuristic=heuriticaManhattan)
    #astarF = astar(problema, heuristic=heuristicaFueraLugar)
    #bestF = bestfs(problema, heuristic=heuristicaFueraLugar)
    #sol_astar = astar(problema, heuristic=nullHeuristic)
    #sol_astar8 = astar(problema, heuristic=heuriticaManhattan)
    #sol_bfs = bfs(problema)
    #sol_ucs = ucs(problema)
    # 2. Llamamos a la función que hace todo el trabajo pesado: 
    #    Ejecuta UCS, ejecuta Best-First, imprime paso a paso y dibuja la tabla.
    #ejecutar_comparativa_desarrolladores(problema)
    print("\n" + "="*70)
    print(" INICIANDO COMPARATIVA: UNIFORM COST SEARCH vs BEST-FIRST SEARCH")
    print("="*70)

    # 1. Ejecutar Uniform Cost Search
    print("\n---> Ejecutando Uniform Cost Search (UCS)...")
    resultado_ucs = ucs(problema)
    print("\n[ Recorrido Estado por Estado - UCS ]")
    imprimir_paso_a_paso(problema, resultado_ucs["Camino"])
    
    # 2. Ejecutar Best First Search con la heuristica de desarrolladores
    print("\n" + "-"*70)
    print("---> Ejecutando Best-First Search (bestfs)...")
    resultado_best = bestfs(problema, heuristic=heuristica_desarrolladores)
    print("\n[ Recorrido Estado por Estado - Best-First Search ]")
    imprimir_paso_a_paso(problema, resultado_best["Camino"])
    #print("\n**** Comparación A* vs Best First ****")
    """
    # h1
    print("\n--- h1: Fuera de lugar ---")
    astarF = astar(problema, heuristic=heuristicaFueraLugar)
    print("A*:", astarF)
    bestF = bestfs(problema, heuristic=heuristicaFueraLugar)
    print("Best First:", bestF)
    # h2
    print("\n--- h2: Manhattan ---")
    astarM = astar(problema, heuristic=heuriticaManhattan)
    print("A*:", astarM)
    bestM = bestfs(problema, heuristic=heuriticaManhattan)
    print("Best First:", bestM)
    print("\n**** Comparacion de bestFirst con ucs ****")
    print("heuristica de desarrolladores ")
    astarD= astar(problema, heuristic=heuristicaDesarrolladores)
    print("A*:", astarD)
    bestD = bestfs(problema, heuristic=heuristicaDesarrolladores)
    print("Best First:", bestD)
    """
if __name__ == "__main__":
    main()