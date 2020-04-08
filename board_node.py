from direction import Direction


class Node:
    def __init__(self, r, c):
        self.owner = None
        self.coordinates = (r, c)
        self.neighbours = {
            Direction.UP: None,
            Direction.UPRIGHT: None,
            Direction.RIGHT: None,
            Direction.DOWN: None,
            Direction.DOWNLEFT: None,
            Direction.LEFT: None,
        }

    def set_neighbours(self, neighbours):
        for direction in neighbours:
            self.set_neighbour(direction, neighbours[direction])

    def set_neighbour(self, direction, neighbour):
        if neighbour:
            self.neighbours[direction] = neighbour
            return True
        else:
            return False

    def get_connected_neighbours(self):
        if self.owner:
            return list(
                filter(lambda neighbour: neighbour and neighbour.owner == self.owner)
            )
        return []

    def __str__(self):
        neighbours_representation = [
            n.coordinates
            for n in filter(lambda neighbour: neighbour, self.neighbours.values())
        ]
        return f"Node: ({self.coordinates}),  Empty: {self.empty}, Neighbours: {neighbours_representation}"

    def __repr__(self):
        return self.__str__()
