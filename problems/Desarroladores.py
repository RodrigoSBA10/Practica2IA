# problems/desarrolladores_bugs.py
# --------------------------------
# Problema inspirado en Misioneros y Caníbales
# Tema: Desarrolladores y Bugs Críticos

class DesarrolladoresBugsProblem:
    # Constructur
    def __init__(self):

        # Estado: (dev_izq, bugs_izq, vehiculo)
        # vehiculo = 0 -> servidor de pruebas (izquierda)
        # vehiculo = 1 -> servidor seguro (derecha)
        #posiciones (desarrolladores, bugs, vehiculo)
        self.start = (3, 3, 0) #Estadp de inicio del problema 
        self.goal = (0, 0, 1) #Meta del problema

        self.total_dev = 3  #Numero de desarroladores 
        self.total_bugs = 3 #Numero de bugs 

        # capacidad máxima del vehículo
        # Diccionario de costos (con clave (tuplas) y valor)
        self.capacidad = 2
        #Se crea una tupla para representar los movimientos y el costo por operacion 
        self.costos = {
            (1, 0): 2,  # 1 Dev
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
        # Extrae el valor actual del estado
        dev_izq, bugs_izq, _ = state     
        #Calcula los desarrolladores del lado derecho
        dev_der = self.total_dev - dev_izq
        bugs_der = self.total_bugs - bugs_izq
       
        #Primer validacion vcerifica que no existan desarrolladores o bugs negativos
        # en ambos lados


        # se calcula cuantos hay en el derecho
        dev_der = self.total_dev - dev_izq
        bugs_der = self.total_bugs - bugs_izq
        # no puede haber valores negativos
        if dev_izq < 0 or bugs_izq < 0:
            return False

        if dev_der < 0 or bugs_der < 0:
            return False
        # Segunda validación:
        # Verifica que no haya más desarrolladores o bugs que el total del sistema
        if dev_izq > self.total_dev or bugs_izq > self.total_bugs:
            return False
        # Tercera validación:
        # En el lado izquierdo, los bugs no pueden superar a los desarrolladores 
        # No puedo haber mas de lo establecido
        if dev_izq > self.total_dev or bugs_izq > self.total_bugs:
            return False
        # No puede haber mas bugs que desarrolladores
        if dev_izq > 0 and bugs_izq > dev_izq:
            return False
        # Cuarta validación:
        # En el lado derecho, los bugs no pueden superar a los desarrolladores
        if dev_der > 0 and bugs_der > dev_der:
            return False

        #Si se cumple las reglas del estado retorna verdadero
        return True

    # --------------------------------
    # Generación de sucesores, los posibles estados
    # --------------------------------

    def getSuccessors(self, state):
        # Estado actual
        dev_izq, bugs_izq, vehiculo = state

        #Se crea una lista para almacenar los estados sucesores 
        # Lista para guardar los estados siguientes
        sucesores = []
        # Los movimientos posibles y permitidos
        movimientos = [
            (0, 2),  # 2 Bugs
            (0, 1),  # 1 Bug
            (1, 1),  # i desarrollador 1 bug
            (2, 0),  # 2 desarrolladores
            (1, 0)   # 1 desarrollador
        ]
        #Itera sobre los movimientos posibles definidos 
        for d, b in movimientos:
            #Verifica que la capacidad del vehiculo
            #si es mayor a lo permitido lo ignora 
            if d + b > self.capacidad:
                continue
            # si la capacidad delvehiculo es cero significa que enviara de lado derecho
            if vehiculo == 0:
              
                #Valida la dispopnibilidad de la izquierda
                if dev_izq < d or bugs_izq < b:
                    continue
                #Genra un nuevo estado
        # recorrer los movimientos
        for d, b in movimientos:
            # No debe exceder la capacidad
            if d + b > self.capacidad:
                continue
            # si el vehiculo esta del lado izquierdo
            if vehiculo == 0:
                # para validar que esten los elementos que se desean mover
                if dev_izq < d or bugs_izq < b:
                    continue
                # Se restan los que se meuven y se cambia el vehiculo
                nuevo_estado = (
                    dev_izq - d,
                    bugs_izq - b,
                    1 #Carrito
                )
                #
                accion = f"Enviar {d} Dev y {b} Bugs"

            else:
                #Calula el laado derecho 
                # calcular los de la derecha
                dev_der = self.total_dev - dev_izq
                bugs_der = self.total_bugs - bugs_izq
                
                #Valida la dispopnibilidad de la derecha
                if dev_der < d or bugs_der < b:
                    continue
                # se regresan al lado izq
                nuevo_estado = (
                    dev_izq + d,
                    bugs_izq + b,
                    0 
                )

                accion = f"Regresar {d} Dev y {b} Bugs"
            #Si se cumple las reglas, guarda el estado valido  
            # solo acepta si el estado es valido
            if self.es_estado_valido(nuevo_estado):

                # cálculo del costo
                costo = (2 * d) + (1 * b)

                #Almacena el estado, la accion realizada y el costo 
                #costo = self.getCostOfActions(accion)
                # se guarda el sucesor por que es valido
                #print("Costo: ", costo)
                sucesores.append(
                    (nuevo_estado, accion, costo)
                )
        # devuelve los sucesores validos
        return sucesores

    # --------------------------------
    # Costo de acciones de la secuendia de acciones
    # --------------------------------

    def getCostOfActions(self, actions):
        #Variable acumuladora 
        costo_total = 0
        #itera las aciones 
        for accion in actions:
            #in sirve para verficar si el contenido esta en la cadena (1,0)
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
        #retorna el costo total
        return costo_total