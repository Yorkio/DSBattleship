from battle_parser import *
import uuid
import pika


"""
#Class to specify the type of the client and send the appropriate requests

# Main methods:

    set_server_id --- bound the client to a given server

    call - make a call using pika and rabbitMQ

    after the method call:
        all the methods that send a request and obtain the appropriate respone from the server
        according to the protocol


"""

class Client:
    def __init__(self, type=0, server_ip='127.0.0.1'):

        self.clientID = str(uuid.uuid1())
        self.server_id = ''
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=server_ip, port=5672))
        self.client_nickname = None
        self.type = type

        self.listen_channel = self.connection.channel()
        self.listen_channel.queue_declare(queue='servers_queue', durable=True)
        self.listen_channel.basic_consume(self.callback,
                              queue='servers_queue',
                              no_ack=True)
        self.server = None

    def set_server_id(self, server_id):
        self.server_id = server_id
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True, durable = True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def get_client_nickname(self):
        return self.client_nickname

    def set_client_nickname(self, nickname):
        self.client_nickname = nickname


    def get_client_id(self):
        return self.clientID

    def get_server_id(self):
        return self.server_id

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def on_response(self, ch, method, props, body):
        if self.corr_id == self.clientID:
            self.response = body

    def callback(self, ch, method, properties, body):
        self.server_name = body

    def get_server(self):
        self.server_name = None
        while self.server_name is None:
            self.connection.process_data_events()
        return self.server_name


    def call(self, request):
        self.response = None

        self.corr_id = self.clientID
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue_durable_' + str(self.server_id),
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                       delivery_mode=2,
                                   ),
                                   body=str(request))

        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def isFreeName(self, name):
        name_request = "#".join(("0", name))

        name_response = self.call(name_request)
        return Parser.parse(name_response)

    def get_game_list(self):
        list_of_games_request = "#".join(("1"))
        list_of_games_response = self.call(list_of_games_request)

        return Parser.parse(list_of_games_response)

    def send_type(self, game_id=None, size=None):
        if self.type == 0:
            game_connection_request = "#".join(("2", "1", game_id))
            print game_connection_request
        elif self.type == 1:
            game_connection_request = "#".join(( "2", "0", size))
        game_connection_response = self.call(game_connection_request)
        return Parser.parse(game_connection_response)

    def send_ships(self, positions):
        positions = "3#" + ''.join(positions)
        server_positions_response = self.call(positions)
        return Parser.parse(server_positions_response)

    def get_number_of_players(self):
        players_requests = "7"
        server_players_repsonse = self.call(players_requests)
        return Parser.parse(server_players_repsonse)


    def new_round_check(self):
        new_round_request = "5"
        server_new_round_response = self.call(new_round_request)
        return Parser.parse(server_new_round_response)

    def handle_shoot(self, isActive, x, y):
        if isActive:
            shoot_request = "4#" + str(x) + ',' + str(y)
        else:
            shoot_request = "4"
        server_shoot_response = self.call(shoot_request)
        return Parser.parse(server_shoot_response)


    def win_check(self):
        new_round_request = "6"
        server_new_round_request = self.call(new_round_request)
        return Parser.parse(server_new_round_request)

    def master_confirm_game(self):
        confirmation = "8"
        server_ackn_master = self.call(confirmation)
        return Parser.parse(server_ackn_master)

    def client_leave(self):
        leave_request = "10"
        server_leave_response = self.call(leave_request)
        return Parser.parse(server_leave_response)

    def become_spectacular(self):
        spectacular_request = "9"
        server_spectacular_response = self.call(spectacular_request)
        return Parser.parse(server_spectacular_response)

    def restart_game_session(self, master, decision):
        restart_request = "11#" + decision
        server_restart_response = self.call(restart_request)
        return Parser.parse(server_restart_response)

    def who_is_master(self):
        master_request = "12"
        server_master_response = self.call(master_request)
        return Parser.parse(server_master_response)