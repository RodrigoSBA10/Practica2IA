# problems/desarrolladores_bugs.py
# --------------------------------
# Problema inspirado en Misioneros y Caníbales
# Tema: Desarrolladores y Bugs Críticos

class DesarrolladoresBugsProblem:

    def __init__(self):

        # Estado: (dev_izq, bugs_izq, vehiculo)
        # vehiculo = 0 -> servidor de pruebas (izquierda)
        # vehiculo = 1 -> servidor seguro (derecha)

        self.start = (3, 3, 0)
        self.goal = (0, 0, 1)

        self.total_dev = 3
        self.total_bugs = 3

        # capacidad máxima del vehículo
        self.capacidad = 2

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

        # Cantidades negativas
        if dev_izq < 0 or bugs_izq < 0:
            return False

        if dev_der < 0 or bugs_der < 0:
            return False

        # Fuera de límites
        if dev_izq > self.total_dev or bugs_izq > self.total_bugs:
            return False

        # Restricción de seguridad en izquierda
        if dev_izq > 0 and bugs_izq > dev_izq:
            return False

        # Restricción de seguridad en derecha
        if dev_der > 0 and bugs_der > dev_der:
            return False

        return True

    # --------------------------------
    # Generación de sucesores
    # --------------------------------

    def getSuccessors(self, state):

        dev_izq, bugs_izq, vehiculo = state

        sucesores = []

        # combinaciones permitidas
        movimientos = [
            (1, 0),  # 1 desarrollador
            (2, 0),  # 2 desarrolladores
            (0, 1),  # 1 bug
            (0, 2),  # 2 bugs
            (1, 1)   # 1 desarrollador y 1 bug
        ]

        for d, b in movimientos:

            # verificar capacidad del vehículo
            if d + b > self.capacidad:
                continue

            # si el vehículo está en la izquierda
            if vehiculo == 0:

                # verificar que haya suficientes elementos
                if dev_izq < d or bugs_izq < b:
                    continue

                nuevo_estado = (
                    dev_izq - d,
                    bugs_izq - b,
                    1
                )

                accion = f"Enviar {d} Dev y {b} Bugs"

            # si el vehículo está en la derecha
            else:

                dev_der = self.total_dev - dev_izq
                bugs_der = self.total_bugs - bugs_izq

                # verificar que haya suficientes elementos
                if dev_der < d or bugs_der < b:
                    continue

                nuevo_estado = (
                    dev_izq + d,
                    bugs_izq + b,
                    0
                )

                accion = f"Regresar {d} Dev y {b} Bugs"

            # validar estado antes de agregarlo
            if self.es_estado_valido(nuevo_estado):

                sucesores.append(
                    (nuevo_estado, accion, 1)
                )

        return sucesores

    # --------------------------------
    # Costo de acciones
    # --------------------------------

    def getCostOfActions(self, actions):

        # costo uniforme
        return len(actions)