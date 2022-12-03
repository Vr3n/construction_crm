import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from pix_apidata import *


class StockConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def addToCeleryBeat(self, watch_list):
        task = PeriodicTask.objects.filter(name="fetch-every-2-seconds")
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in watch_list:
                if x not in args:
                    args.append(x)
            print(args)
            task.args = json.dumps([[args]])
            print(task)
            task.save()
        else:
            schedule, create = IntervalSchedule.objects.get_or_create(
                every=2, period=IntervalSchedule.SECONDS)

            task = PeriodicTask.objects.create(
                interval=schedule, name="fetch-every-2-seconds", task="api.tasks.update_stock_prices", args=json.dumps([[watch_list]])
            )

    async def connect(self):
        self.room_group_name = 'stock_update'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # add to celery beat
        await self.addToCeleryBeat(
            ['8KMILES', '3MINDIA', '20MICRONS']
        )

        await self.accept()

    async def disconnect(self):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_stock_update',
                'message': message
            }
        )

    # Receive message from room group
    async def send_stock_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class OrderUpdatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "order_updates"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'notificaton',
            'message': message,
        })

    async def notification(self, event):
        await self.send(text_data=json.dumps(event))


class AdminNotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "admin_notifications"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'notificaton',
            'message': message,
        })

    async def notification(self, event):
        await self.send(text_data=json.dumps(event))


class AdminFundsUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.room_group_name = "admin_fund_updates"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'funds_update',
            'message': message,
        })

    async def funds_update(self, event):
        await self.send(text_data=json.dumps(event))

# class AccelpixStockConsumer(AsyncConsumer):

#     def __init__(self):
#         # self.watch_list = watch_list
#         self.api = apidata_lib.ApiData()
#         try:
#             self.loop = asyncio.get_event_loop()
#         except RuntimeError:
#             self.loop = asyncio.new_event_loop()

#     def on_trade(msg):
#         trd = apidata_models.Trade(msg)
#         # or print(trd.volume) likewise object can be called for id, kind, ticker, segment, price, qty, oi
#         print("Trade : ", msg, "\n")
#         # return msg

#     def on_best(msg):
#         bst = apidata_models.Best(msg)
#         # or print(bst.bidPrice) likewise object can be called for ticker, segmentId, kind, bidQty, askPrice, askQty
#         # print("Best.BidPrice : ", bst.bidPrice, "\n")
#         print(msg)

#     def on_refs(msg):
#         ref = apidata_models.Refs(msg)
#         # or print(ref.price) likewise object can be called for segmentId, kind, ticker
#         print(msg)

#     def on_srefs(msg):
#         sref = apidata_models.RefsSnapshot(msg)
#         # or print(sref.high) likewise object can be called for kind, ticker, segmentId, open, close, low, avg, oi, lpc,upc
#         print(msg)

#     def connection_started():
#         print("Connection started callback")

#     def connection_stopped():
#         print("Connection stopped callback")

#     async def main(self):
#         self.api.on_connection_started(self.connection_started)
#         self.api.on_connection_stopped(self.connection_stopped)
#         self.api.on_trade_update(on_trade)
#         self.api.on_best_update(on_best)
#         self.api.on_refs_update(on_refs)
#         self.api.on_srefs_update(on_srefs)

#         key = "/745y8A+XPshmfCGilWWDfgzrJo="
#         host = "apidata.accelpix.in"
#         scheme = "http"
#         s = await api.initialize(key, host,scheme)
#         print(s)

#         his = await api.get_intra_eod("NIFTY-1","20210603", "20210604", "5")
#         print("History : ",his)

#         syms = ['NIFTY-1', 'BANKNIFTY-1', "INFY", "AARTIIND",]

#         await api.subscribeAll(syms)
#         print("subscribe done")

#     def run():
#         event_loop = self.loop
#         event_loop.create_task(self.main())
#         try:
#             event_loop.run_forever()
#         finally:
#             event_loop.close()
