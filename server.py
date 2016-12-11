import uuid
from Queue import Queue
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

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


GameSessions = []

class Parser:
    @staticmethod
    def parse(request):
        subrequests = request.split('#')
        if (len(subrequests) == 0):
            return
        if (subrequests[0] == '1'):
            response = 'ft'
            for game in GameSessions:
                response += '1'
            return response



def on_request(ch, method, props, body):
    request = str(body)

    response = Parser.parse(request)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()