# Ejecuta DFS/BFSUCS/A* sobre el problema de las jarras.

from search import dfs, bfs, ucs, astar, bestfs, nullHeuristic, dls, iddfs, heuristicaDesarrolladores, imprimir_solucion, heuriticaManhattan, heuristicaFueraLugar
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


    print("\n**** Comparación A* vs Best First vs UCS ****")

    # h1
    print("\n--- Heuristica Desarrolladores ---")
    astarF = astar(problema, heuristic=heuristicaDesarrolladores)
    print("A*:", astarF)
    bestF = bestfs(problema, heuristic=heuristicaDesarrolladores)
    print("Best First:", bestF)
    print("UCS")
    sol_ucs = ucs(problema)
    print("UCS:", sol_ucs)

    # h2
    """
    print("\n--- h2: Manhattan ---")
    astarM = astar(problema, heuristic=heuriticaManhattan)
    print("A*:", astarM)
    bestM = bestfs(problema, heuristic=heuriticaManhattan)
    print("Best First:", bestM)
    """
if __name__ == "__main__":
    main()