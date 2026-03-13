# main.py
# ------
# Prueba simple de DFS/BFS/UCS/A* con un grafo pequeño.

# Ejecuta DFS/BFSUCS/A* sobre el problema de las jarras.

from search import dfs, bfs, ucs, astar,dfs_sin, nullHeuristic
from search import dfs, bfs, ucs, astar, nullHeuristic, dls, iddfs
from problems.Desarroladores import DesarrolladoresBugsProblem

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
    sol_bfs = bfs(problema)
    sol_ucs = ucs(problema)
    sol_astar = astar(problema, heuristic=nullHeuristic)  # con h=0, A* = UCS
    sol_iddfs = iddfs(problema, 15)
    sol_dls = dls(problema, 2)

    """
    print("========================================")
    print(" Problema de las Jarras")
    print(" Capacidad A =", problema.capA, " Capacidad B =", problema.capB)
    print(" Inicio =", problema.start, " Meta =", problema.goal)
    print("========================================\n")
    """
    print("BFS (menos pasos):")
    print(sol_bfs)
    print("Costo:", problema.getCostOfActions(sol_bfs))
    print()

    print("UCS (menor costo):")
    print(sol_ucs)
    print("Costo:", problema.getCostOfActions(sol_ucs))
    print()


    print("astar (puede no ser óptimo):")
    print(astar)
    print("Costo:", problema.getCostOfActions(sol_astar))


    # Si quieres ver DFS también (ojo: puede dar rutas largas dependiendo del orden de sucesores)
    sol_dfs = dfs(problema)
    print("DFS (puede no ser óptimo):")
    print(sol_dfs)
    print("Costo:", problema.getCostOfActions(sol_dfs))
    print()


    #DFS sin visitados
    dfs_sin_vis = dfs_sin(problema)
    print("DFS Arbol sin visitados")
    print(dfs_sin_vis)
    print("Costo:", problema.getCostOfActions(dfs_sin_vis)) 
   

    print("A* (puede no ser óptimo):")
    print(sol_astar)
    print("Costo:", problema.getCostOfActions(sol_astar))
    print()

    print("IDDFS")
    print(sol_iddfs)
    print("Costo:", problema.getCostOfActions(sol_iddfs))


if __name__ == "__main__":
    main()




