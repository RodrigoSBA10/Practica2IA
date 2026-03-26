# problems/desarrolladores_bugs.py
# --------------------------------
# Problema inspirado en Misioneros y Caníbales
# Tema: Desarrolladores y Bugs Críticos

class DesarrolladoresBugsProblem:

    def __init__(self):

        # Estado: (dev_izq, bugs_izq, vehiculo)
        # vehiculo = 0 -> servidor de pruebas (izquierda)
        # vehiculo = 1 -> servidor seguro (derecha)

        self.start = (3, 3, 0)  #Estado inicial 
        self.goal = (0, 0, 1) #Estado Final

        self.total_dev = 3 #numero de desarrolladores 
        self.total_bugs = 3 #numero de bugs

        # capacidad máxima del vehículo
        self.capacidad = 2
        self.costos = {
            (1, 0): 2,  # 1 Dev estos son las tuplas ()
            (2, 0): 4,  # 2 Dev
            (0, 1): 1,  # 1 Bug
            (0, 2): 2,  # 2 Bugs
            (1, 1): 3   # 1 Dev y 1 Bug
        }

    # --------------------------------
    # Estado inicial
    # --------------------------------

    def getStartState(self):
        return self.start

    # --------------------------------
    # Verificación de meta
    # --------------------------------

    def isGoalState(self, state):
        return state == self.goal

    # --------------------------------
    # Verificación de restricciones
    # --------------------------------

    def es_estado_valido(self, state):

        dev_izq, bugs_izq, _ = state

        dev_der = self.total_dev - dev_izq
        bugs_der = self.total_bugs - bugs_izq

        if dev_izq < 0 or bugs_izq < 0:
            return False

        if dev_der < 0 or bugs_der < 0:
            return False

        if dev_izq > self.total_dev or bugs_izq > self.total_bugs:
            return False

        if dev_izq > 0 and bugs_izq > dev_izq:
            return False

        if dev_der > 0 and bugs_der > dev_der:
            return False

        return True

    # --------------------------------
    # Generación de sucesores
    # --------------------------------

    def getSuccessors(self, state):

        dev_izq, bugs_izq, vehiculo = state

        sucesores = []

        movimientos = [
            (1, 0),  # 1 desarrollador
            (2, 0),  # 2 desarrolladores
            (0, 1),  # 1 bug
            (0, 2),  # 2 bugs
            (1, 1)   # 1 desarrollador y 1 bug
        ]

        for d, b in movimientos:

            if d + b > self.capacidad:
                continue

            if vehiculo == 0:

                if dev_izq < d or bugs_izq < b:
                    continue

                nuevo_estado = (
                    dev_izq - d,
                    bugs_izq - b,
                    1
                )

                accion = f"Enviar {d} Dev y {b} Bugs"

            else:

                dev_der = self.total_dev - dev_izq
                bugs_der = self.total_bugs - bugs_izq

                if dev_der < d or bugs_der < b:
                    continue

                nuevo_estado = (
                    dev_izq + d,
                    bugs_izq + b,
                    0
                )

                accion = f"Regresar {d} Dev y {b} Bugs"

            if self.es_estado_valido(nuevo_estado):

                # cálculo del costo según tu tabla
                costo = (2 * d) + (1 * b)

                sucesores.append(
                    (nuevo_estado, accion, costo)
                )

        return sucesores

    # --------------------------------
    # Costo de acciones
    # --------------------------------

    def getCostOfActions(self, actions):

        costo_total = 0

        for accion in actions:

            if "1 Dev y 0 Bugs" in accion:
                costo_total += self.costos[(1,0)]

            elif "2 Dev y 0 Bugs" in accion:
                costo_total += self.costos[(2,0)]

            elif "0 Dev y 1 Bugs" in accion:
                costo_total += self.costos[(0,1)]

            elif "0 Dev y 2 Bugs" in accion:
                costo_total += self.costos[(0,2)]

            elif "1 Dev y 1 Bugs" in accion:
                costo_total += self.costos[(1,1)]

        return costo_total