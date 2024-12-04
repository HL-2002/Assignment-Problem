from munkres import Munkres, print_matrix
import sys


class Matrix:
    """Matrix class to represent a matrix and perform operations on it.

    Attributes:
        array (list[list[float]]): A 2D list representing the matrix.
    """

    array: list[list[float]] = []

    def __init__(self, array: list[list[int]]) -> None:
        self.array = array

    def validate(self) -> bool:
        # Validate rectangular or square matrix
        # TODO: Refactor to use all() instead of False in, reserved for OUR implementation, not Kenny's.
        if False in (len(row) == len(self.array[0]) for row in self.array):
            print(
                "Error: Irregular matrix no allowed, it must be rectangular or square."
            )
            return False
        # Validate matrix values
        for row in self.array:
            for value in row:
                # Value check
                if value < 0:
                    print("Error: Matrix values must be greater than 0")
                    return False

        return True

    # Algorithm's source: https://software.clapper.org/munkres/
    def munkres(self) -> None:
        m: Munkres = Munkres()
        indexes = m.compute(self.array)

        print_matrix(self.array, msg="Lowest cost through this matrix:")
        total = 0
        for row, column in indexes:
            value = self.array[row][column]
            total += value
            print(f"({row}, {column}) -> {value}")
        print(f"Total cost: {total}")

    def in_house(self) -> None:
        # Validate square matrix
        dif: int = len(self.array) - len(self.array[0])
        # More rows than columns
        if dif > 0:
            for row in self.array:
                row.extend([0] * dif)
        # More columns than rows
        elif dif < 0:
            for _ in range(abs(dif)):
                self.array.append([0] * len(self.array[0]))

        # Permutations
        results = []
        self._permute(range(len(self.array)), results)
        # Calculate cost
        min_cost: float = sys.maxsize
        min_indexes: list[int] = []

        for indexes in results:
            cost = 0
            for row, col in enumerate(indexes):
                cost += self.array[row][col]
            if cost < min_cost:
                min_cost = cost
                min_indexes = indexes

        # Print results
        for row, col in enumerate(min_indexes):
            print(f"({row}, {col}) -> {self.array[row][col]}")
        print(f"Total cost: {min_cost}")

    def _permute(self, agents: list[int], results: list[list[int]]) -> None:
        """Recursively generates all permutations of the given list of agents and stores them in the results list.

        This method uses a recursive approach to generate permutations. For each agent in the list, it removes the agent,
        generates all permutations of the remaining agents, and then prepends the removed agent to each of these permutations.
        The resulting permutations are added to the results list.

        Args:
            agents (list[int]): List of agents to permute.
            results (list[list[int]]): List to store the generated permutations. Each permutation is a list of integers
                                       representing the order of agents.

        Example:
            Given agents = [0, 1, 2], the results list will be populated with:
            [   
                [0, 1, 2],
                [0, 2, 1],
                [1, 0, 2],
                [1, 2, 0],
                [2, 0, 1],
                [2, 1, 0]
            ]
            \nWhere [0, 2, 1] means agent 0 is assigned to task 2, agent 1 to task 2, and agent 2 to task 1.
        """
        # TODO: Alternative implementation that returns the permutations as a (agent, task) tuple list, again, reserved for OUR implementation, not Kenny's.
        # Doing it will need to change the cost calculation to use the tuples instead of building the enumeration.
        # Doing all of that will need to change the docstring to reflect the new implementation.
        if len(agents) == 1:
            results.insert(len(results), agents)
        else:
            for i in range(len(agents)):
                element = agents[i]
                agents_copy = [agents[j] for j in range(len(agents)) if j != i]
                subresults = []
                self._permute(agents_copy, subresults)
                for subresult in subresults:
                    result = [element] + subresult
                    results.insert(len(results), result)


def main():
    # Create matrix (input from user)
    array: list[list[float]] = []
    # Outer loop to create and validate the matrix
    while True:
        # Inner loop to input matrix rows
        while True:
            line: str = input(
                "Enter matrix row (separate values by comma, whitespace to terminate): "
            )
            if line == "":
                break
            try:
                array.append([float(value) for value in line.split(",")])
            except ValueError:
                print("Error: Invalid input. Please enter numbers only.")

        matrix: Matrix = Matrix(array)

        # TODO: Validation can be done while appending to array, so the matrix is traversed only once, but that's reserved for OUR implementation, not Kenny's.
        if matrix.validate():
            break
        else:
            array = []
            print("Error: Invalid matrix, please re-enter.")

    # Select criteria (Time or Cost optimization)
    criteria: str = ""
    while True:
        criteria = input("Select criteria (Time or Cost): ")
        # Validate criteria
        if criteria.lower() not in ["time", "cost"]:
            print("Error: Invalid criteria. Please select Time or Cost.")
        else:
            break

    # Select algorithm (Munkres, in-house)
    option: int = 0
    while True:
        option = int(input("Select algorithm (1. Munkres, 2. In-house): "))
        # Validate option
        if option not in [1, 2]:
            print("Error: Invalid option. Please select 1 or 2.")
        else:
            break

    # Execute algorithm
    if option == 1:
        matrix.munkres()
    else:
        matrix.in_house()


if __name__ == "__main__":
    main()
