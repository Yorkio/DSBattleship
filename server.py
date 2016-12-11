import uuid
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

class GameSession:
    def __init__(self, login, ip):
        self.id = uuid.uuid4()
        self.players = {}
        self.ships = []
        player = Player(login, ip)
        self.master_client = login
        self.players[login] = player
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
    def addPlayer(self, login, id):
        player = Player(login, id)
        self.players[login] = player

    def addShipsOfPlayer(self, id, message):
        ships = message.split(';')
        for i in range(len(ships)):
            entity = ships[i].split(',')
            x = int(entity[0])
            y = int(entity[1])
            length = int(entity[2])
            direction = entity[3]       # 0 - horizontal, 1 - vertical
            coordinates = []
            if direction == '0':
                for j in range(length):
                    coordinates.append((x, y + j))
            elif direction == '1':
                for j in range(length):
                    coordinates.append((x + j, y))
            ship = Ship(id, length, coordinates)
            self.ships.append(ship)
        return 0

    def startGame(self):
        return 0

    def receiveStartGame(self):
        self.startGame()

class Game(GameSession):
    def currentActivePlayers(self):
        count = 0
        for player in self.players:
            if player.type == "Player":
                count += 1
        return count

    def makeHit(self, login, coordinate):
        hit_conditions = {}    # values: 0 - missed, 1 - hitted, 2 - sinked, 3 - hiter; keys: players
        hit_conditions[login] = 3
        for i in range(len(self.ships)):
            if self.ships[i].owner_login != login and coordinate in self.ships[i].coordinates:
                self.ships[i].coordinates.remove(coordinate)
                if len(self.ships[i].coordinates) == 0:
                    hit_conditions[self.ships[i].owner_login] = 2
                else:
                    hit_conditions[self.ships[i].owner_login] = 1
        for player in self.players.keys():
            if player not in hit_conditions.keys():
                hit_conditions[player] = 0
        return 0

    def sendStats(self, hit_conditions, correlation_IDs):
        messages = dict.fromkeys(self.players.keys(), '')
        for player in self.players.keys():          # 3# + 0 - this player wasn't hitted, 1 - this player wasn't hitted + # list of players which ships was sinked
            if hit_conditions[player] == 0:
                messages[player] += '3#0#'
            elif hit_conditions[player] == 1:
                messages[player] += '3#1#'
        for player in hit_conditions:
            if hit_conditions[player] == 2:
                for p in self.players:
                    messages[p] += player + ';'
        for player in self.players.keys():
            messages[player]  = messages[player][:len(messages[player]) - 1] + '#'
        for player in self.players.keys():
            response = messages[player]
            correlation_id = correlation_IDs[player]
            channel.basic_publish(exchange='',
                                    routing_key='',
                                    properties=pika.BasicProperties(correlation_id = correlation_id),
                                    body=str(response))

    def checkEndGame(self):
        owner = self.ships[0].owner_login
        for i in range(1, len(self.ships)):
            if self.ships[i].owner_login != owner:
                return False
        return True

class Ship:
    def __init__(self, owner_login, length, coordinates):
        self.length = length
        self.coordinates = coordinates
        self.owner_login = owner_login

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
                    numOfActiveGames += 1
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
