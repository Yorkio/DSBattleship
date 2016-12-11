from battle_board import *
from battle_login import *
from battle_parser import *
import uuid
import pika
import time

class Client:
    def __init__(self, server_ip):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=server_ip))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None

        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def check_name(self):

        name_request = "#".join(("0", name))
        name_response = self.call(name_request)
        print name_response
        return Parser.parse(name_response)

    def get_game_list(self):
        list_of_games_request = "#".join(("1"))
        list_of_games_responce = self.call(list_of_games_request)
        return list_of_games_responce


client = Client("127.0.0.1")
name = raw_input("Enter the name")
while not client.check_name(name):
    print client.check_name(name)
    name = raw_input()


while True:
    time.sleep(3)
    print client.get_game_list()




