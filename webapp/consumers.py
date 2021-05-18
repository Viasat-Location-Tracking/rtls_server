import json
from channels.generic.websocket import JsonWebsocketConsumer

class MapConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
    
    def receive(self, json_data):
        self.send(json_data=json_data)