from battle_parser import *
import uuid
import pika
import time




class Client:
    def __init__(self, server_id=None, type=0 , server_ip='127.0.0.1'):

        self.clientID = str(uuid.uuid1())
        self.server_id = server_id
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=server_ip, port=5672))

        self.type = type

        self.listen_channel = self.connection.channel()
        self.listen_channel.queue_declare(queue='servers_queue', durable=True)
        self.listen_Gchannel.basic_consume(self.callback,
                              queue='servers_queue',
                              no_ack=True)
        self.server = None

    def set_server_id(self, server_id):
        self.server_id = server_id
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='rpc_queue_durable_' + server_id, exclusive=True, durable = True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=result)

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


    def call(self, n):
        self.response = None

        self.corr_id = self.clientID

        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue_durable_' + str(self.server_id),
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def isFreeName(self, name):
        name_request = "#".join(("0", name))
        name_response = self.call(name_request)
        print name_response
        return Parser.parse(name_response)

    def get_game_list(self):
        list_of_games_request = "#".join(("1"))
        list_of_games_response = self.call(list_of_games_request)
        return Parser.parse(list_of_games_response)

    def send_type(self, game_id=None, size=None):
        if self.type == 0:
            game_connection_request = "#".join(("2", "1", game_id))
        elif self.type == 1:
            game_connection_request = "#".join(( "2", "0", size))
        game_connection_response = self.call(game_connection_request)
        return Parser.parse(game_connection_response)

    def send_ships(self, positions):
        positions = "#3#" + "#".join(positions)
        server_positions_response = self.call(positions)
        return Parser.parse(server_positions_response)
