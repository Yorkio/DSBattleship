class Ship:
    def __init__(self, size):
        self.size = size
        self.position = []
        self.breakouts = []
        self.hp = size

    def get_position(self):
        return self.position

    def set_position(self, coordinates):
        assert self.size >= self.size, "Reached the maximum size of the ship"
        self.position.append(coordinates)

    def shoot(self, coordinates):
        if coordinates in self.position and coordinates not in self.breakouts:
            self.breakouts.append(coordinates)
            self.hp -= 1

    def isDestroyed(self):
        if self.hp == 0:
            return True

