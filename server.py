import uuid
from Queue import Queue
import pika
import os

class GameSession:
    def __init__(self, id):
        self.id = uuid.uuid4()
        self.ships = []
        self.players = Queue()
        self.master_client_id = id

    def disconnect(self, player_id):
        return 0

    def leave(self, player_id):
        return 0

class Wait(GameSession):
    def addPayer(self, login, id):
        player = Player(login, id)
        self.players.put(player)

    def addShipsOfPlayer(self, id, ships):

        return 0

    def sendStats(self):
        return 0

    def startGame(self):
        return 0

    def receiveStartGame(self):
        self.startGame()

class Game(GameSession):
    def currentActivePlayers(self):
        return 0

    def makeHit(self):
        return 0

    def sendStats(self):
        return 0

    def checkEndGame(self):
        return 0

class Ship:
    def __init__(self, length, start, direction):
        self.length = length
        self.coordinates = []

class Player:
    def __init__(self, login, id):
        self.id = id
        self.login = login
        self.score = 0
        self.type = 'Player'  # Spectator, Leaved

game = GameSession(1)
print game.id
