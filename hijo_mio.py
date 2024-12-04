from munkres import Munkres, print_matrix
import sys


class Matriz:
    """Clase Matriz para representar una matriz y realizar operaciones en ella.

    Atributos:
        arreglo (list[list[float]]): Una lista 2D que representa la matriz.
    """

    arreglo: list[list[float]] = []

    def __init__(self, arreglo: list[list[int]]) -> None:
        self.arreglo = arreglo

    def validar(self) -> bool:
        # Validar matriz rectangular o cuadrada
        if False in (len(fila) == len(self.arreglo[0]) for fila in self.arreglo):
            print(
                "Error: Matriz irregular no permitida, debe ser rectangular o cuadrada."
            )
            return False
        # Validar valores de la matriz
        for fila in self.arreglo:
            for valor in fila:
                # Verificación de tipo
                if not isinstance(valor, int) and not isinstance(valor, float):
                    print("Error: Los valores de la matriz deben ser números.")
                    return False
                # Verificación de valor
                if valor < 0:
                    print("Error: Los valores de la matriz deben ser mayores que 0")
                    return False

        return True

    def munkres(self) -> None:
        m: Munkres = Munkres()
        indices = m.compute(self.arreglo)

        print_matrix(self.arreglo, msg="Costo más bajo a través de esta matriz:")
        total = 0
        for fila, columna in indices:
            valor = self.arreglo[fila][columna]
            total += valor
            print(f"({fila}, {columna}) -> {valor}")
        print(f"Costo total: {total}")

    def en_casa(self) -> None:
        # Validar matriz cuadrada
        dif: int = len(self.arreglo) - len(self.arreglo[0])
        # Más filas que columnas
        if dif > 0:
            for fila in self.arreglo:
                fila.extend([0] * dif)
        # Más columnas que filas
        elif dif < 0:
            for _ in range(abs(dif)):
                self.arreglo.append([0] * len(self.arreglo[0]))

        # Permutaciones
        resultados = []
        self.permutar(range(len(self.arreglo)), resultados)
        # Calcular costo
        costo_min: float = sys.maxsize
        indices_min: list[int] = []

        for indices in resultados:
            costo = 0
            for fila, col in enumerate(indices):
                costo += self.arreglo[fila][col]
            if costo < costo_min:
                costo_min = costo
                indices_min = indices

        # Imprimir resultados
        for fila, col in enumerate(indices_min):
            print(f"({fila}, {col}) -> {self.arreglo[fila][col]}")
        print(f"Costo total: {costo_min}")

    def permutar(self, agentes: list[int], resultados: list[list[int]]) -> None:
        """Genera recursivamente todas las permutaciones de la lista dada de agentes y las almacena en la lista de resultados.

        Este método utiliza un enfoque recursivo para generar permutaciones. Para cada agente en la lista, elimina el agente,
        genera todas las permutaciones de los agentes restantes, y luego antepone el agente eliminado a cada una de estas permutaciones.
        Las permutaciones resultantes se agregan a la lista de resultados.

        Args:
            agentes (list[int]): Lista de agentes a permutar.
            resultados (list[list[int]]): Lista para almacenar las permutaciones generadas. Cada permutación es una lista de enteros
                                          que representa el orden de los agentes.

        Ejemplo:
            Dado agentes = [0, 1, 2], la lista de resultados se poblará con:
            [   
                [0, 1, 2],
                [0, 2, 1],
                [1, 0, 2],
                [1, 2, 0],
                [2, 0, 1],
                [2, 1, 0]
            ]
            \nDonde [0, 2, 1] significa que el agente 0 está asignado a la tarea 2, el agente 1 a la tarea 2, y el agente 2 a la tarea 1.
        """
        if len(agentes) == 1:
            resultados.insert(len(resultados), agentes)
        else:
            for i in range(len(agentes)):
                elemento = agentes[i]
                copia_agentes = [agentes[j] for j in range(len(agentes)) if j != i]
                subresultados = []
                self.permutar(copia_agentes, subresultados)
                for subresultado in subresultados:
                    resultado = [elemento] + subresultado
                    resultados.insert(len(resultados), resultado)


def main():
    # Crear matriz (entrada del usuario)
    arreglo: list[list[float]] = []
    # Bucle externo para crear y validar la matriz
    while True:
        # Bucle interno para ingresar filas de la matriz
        while True:
            linea: str = input(
                "Ingrese fila de la matriz (separe los valores con coma, espacio en blanco para terminar): "
            )
            if linea == "":
                break
            try:
                arreglo.append([float(valor) for valor in linea.split(",")])
            except ValueError:
                print("Error: Entrada inválida. Por favor ingrese solo números.")

        matriz: Matriz = Matriz(arreglo)

        if matriz.validar():
            break
        else:
            arreglo = []
            print("Error: Matriz inválida, por favor reingrese.")

    # Seleccionar criterio (Optimización de Tiempo o Costo)
    criterio: str = ""
    while True:
        criterio = input("Seleccione criterio (Tiempo o Costo): ")
        # Validar criterio
        if criterio.lower() not in ["tiempo", "costo"]:
            print("Error: Criterio inválido. Por favor seleccione Tiempo o Costo.")
        else:
            break

    # Seleccionar algoritmo (Munkres, en casa)
    opcion: int = 0
    while True:
        opcion = int(input("Seleccione algoritmo (1. Munkres, 2. Pan de jamón): "))
        # Validar opción
        if opcion not in [1, 2]:
            print("Error: Opción inválida. Por favor seleccione 1 o 2.")
        else:
            break

    # Ejecutar algoritmo
    if opcion == 1:
        matriz.munkres()
    else:
        matriz.en_casa()


if __name__ == "__main__":
    main()