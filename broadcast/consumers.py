import json
from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer

class AdminNotificationConsumer(AsyncConsumer):

    def __init__(self, *args, **kwargs):
        self.room_group_name = None
        self.room_name = None
        self.room = None

    async def connect(self, event):
        self.room_group_name = "admin_notifications"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name)
        print(self.room_group_name)
        print(self.channel_name)

        self.accept()

    async def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    async def receive(self, event):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send({
            "type": "notification",
            "message": message,
        })

    async def notification(self, event):
        self.send(text_data=json.dumps(event))
