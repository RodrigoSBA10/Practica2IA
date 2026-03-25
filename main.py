# main.py
# ------
# Prueba simple de DFS/BFS/UCS/A* con un grafo pequeño.

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
    #problema = DesarrolladoresBugsProblem()
    problema = OchoPuzzle((1,3,4,2,5,6,7,0,8))
    #sol_astar = astar(problema, heuristic=nullHeuristic)
    #sol_astar8 = astar(problema, heuristic=heuriticaManhattan)
    sol_bfs = bfs(problema)
    #sol_ucs = ucs(problema)


# ************* PARTE 2 BEST COMPRACION A* VS FIRST SEARCH ***************
#   Best First Search
    print("\n\n**** Comparaciòn A* vs Best First **** ")

#   h1: Fuera de Lugar
    print("\n*********************************** h1: Fichas fuera de lugar *************************************\n")

    sol_a1 = astar(problema, heuristic=heuristicaFueraLugar)
    print("A* h1:", sol_a1)
    print("Costo:", problema.getCostOfActions(sol_a1))

    sol_b1 = bestfs(problema, heuristic=heuristicaFueraLugar)
    print("Best First h1:", sol_b1)
    print("Costo:", problema.getCostOfActions(sol_b1))

#   h2: Manhattan 
    print("\n\n\n*********************************** h2: Manhattan *************************************\n")

    sol_a2 = astar(problema, heuristic=heuriticaManhattan)
    print("A* h2:", sol_a2)
    print("Costo:", problema.getCostOfActions(sol_a2))

    sol_b2 = bestfs(problema, heuristic=heuriticaManhattan)
    print("Best First h2:", sol_b2)
    print("Costo:", problema.getCostOfActions(sol_b2))
# ************* PARTE 2 BEST COMPRACION A* VS FIRST SEARCH ***************


    
    #sol_astar = astar(problema, heuristic=nullHeuristic)  # con h=0, A* = UCS
    #sol_astarHeuristica = astar(problema, heuristicaDesarrolladores)
    #sol_iddfs = iddfs(problema, 15)
    #sol_dls = dls(problema, 2)
    """
    print("========================================")
    print(" Problema de las Jarras")
    print(" Capacidad A =", problema.capA, " Capacidad B =", problema.capB)
    print(" Inicio =", problema.start, " Meta =", problema.goal)
    print("========================================\n")
    """
#     print("BFS (menos pasos):")
#     print(sol_bfs)
#     print("Costo:", problema.getCostOfActions(sol_bfs))
#     print()
    """
    # Si quieres ver DFS también (ojo: puede dar rutas largas dependiendo del orden de sucesores)
    sol_dfs = dfs(problema)
    print("DFS (puede no ser óptimo):")
    print(sol_dfs)
    print("Costo:", problema.getCostOfActions(sol_dfs))
    print()

    print("A*")
    print(sol_astar)
    print("Costo:" , problema.getCostOfActions(sol_astar))
    print()
    """


    #print("A* heuristica")
    #print(sol_astarHeuristica)
    #imprimir_solucion(problema, sol_astarHeuristica)
    #print("Costo:" , problema.getCostOfActions(sol_astarHeuristica))
    #print()
    """
    print("A* heuristica")
    print(sol_astar)
    #imprimir_solucion(problema, nullHeuristic)
    print("Costo:" , problema.getCostOfActions(sol_astar))
    print()
    
    print("A* heuristica")
    print(sol_astar8)
    #imprimir_solucion(problema, nullHeuristic)
    print("Costo:" , problema.getCostOfActions(sol_astar8))
    print()
    """
    """
    print("A* heuristica")
    print(sol_astar)
    #imprimir_solucion(problema, sol_astar)

    print("UCS (menor costo):")
    print(sol_ucs)
    print("Costo:", problema.getCostOfActions(sol_ucs))
    print()

    print("A* (puede no ser óptimo):")
    print(sol_astar)
    print("Costo:", problema.getCostOfActions(sol_astar))
    print()

    print("IDDFS")
    print(sol_iddfs)
    print("Costo:", problema.getCostOfActions(sol_iddfs))
    """
if __name__ == "__main__":
    main()




