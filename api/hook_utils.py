import requests
import channels.layers
from asgiref.sync import async_to_sync

def update_available_margin(fund_obj, margin):
    """
    Updating the available margin for for the User fund.

    Accepts the Fund Object and Modifies the available margin as per the
    margin specified in the order

    fund_obj: UserFund Object
    margin: str
    """
    fund_obj.available_margin = str(float(fund_obj.available_margin) - float(
        margin))
    fund_obj.used_margin = str(float(fund_obj.used_margin) + float(margin))
    fund_obj.save()

def send_notification(room_name: str, msg: str):
    """
    Utility function to Send Custom notifications,
    to the Channels.

    room_name: str -> Channel room name you want to send notification.
    msg: str -> notification message to channel room.
    """

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_name, {
        'type': 'notification',
        'message': msg
    })


def send_sms(receiver_mobile_number: list, message: str, template_id: str):
    # SMS_ENDPOINT = "http://login.swarajinfotech.com/domestic/sendsms/jsonapi.php"

    if isinstance(receiver_mobile_number, str):
        receiver_mobile_number = [receiver_mobile_number]

    SMS_URL = f"http://login.swarajinfotech.com/domestic/sendsms/bulksms_v2.php?apikey={os.environ.get('SMS_APIKEY')}&templateId={template_id}&type=TEXT&sender={os.environ.get( 'SMS_SENDER' )}&mobile={','.join([str(x) for x in receiver_mobile_number])}&message={message}"

    # HEADERS = {
    #     'apiKey': SMS_APIKEY
    # }
    # BODY = {
    #     "data": [{
    #         "destination": receiver_mobile_number[0],
    #         "source": SMS_SENDER,
    #         "type": "0",
    #         "content": message,
    #     }]
    # }

    # res = requests.post(SMS_ENDPOINT, headers=HEADERS, json=BODY)
    res = requests.post(SMS_URL)
    print("Post request sent!")
    print(res)
    if res.status_code == 200:
        print("Successfull")

    print(res.content)