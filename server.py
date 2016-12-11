import uuid
from Queue import Queue
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

class GameSession:
    def __init__(self, login, ip):
        self.id = uuid.uuid4()
        self.players = []
        self.ships = []
        player = Player(login, ip)
        self.master_client = login
        self.players.append(player)
        self.state = 0
        self.size = 10

    def __init__(self, login, ip, size):
        self.id = uuid.uuid4()
        self.ships = []
        self.players = []
        self.master_client = login
        player = Player(login, ip)
        self.players.append(player)
        self.state = 0
        self.size = size

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
    def __init__(self, login, ip):
        self.ip = ip
        self.login = login
        self.score = 0
        self.type = 'Player'  # Spectator, Leaved

Players = {}
GameSessions = []

class Parser:
    @staticmethod
    def parse(request):
        subrequests = request.split('#')
        if (len(subrequests) == 0):
            return

        if (subrequests[0] == '0'):
            if (len(subrequests) < 3):
                return
            request_name = subrequests[1]
            response = 0
            if (request_name in Players.keys()):
                response = '0#0'
                return response
            player_ip = subrequests[2]
            Players[request_name] = Player(request_name, player_ip)
            response = '0#1'
            return response

        if (subrequests[0] == '1'):
            response = '1#'
            response_tail = ''
            numOfActiveGames = 0
            for game in GameSessions:
                if (game.state == 0):
                    ++numOfActiveGames
                    response_tail += str(game.id) + '#'
                    response_tail += str(game.size) + '#'
                    response_tail += str(len(game.players)) + '#'
            return response + str(numOfActiveGames) + '#' + response_tail



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