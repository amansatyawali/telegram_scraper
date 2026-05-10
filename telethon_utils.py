from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
import pandas as pd
import datetime


def get_chats(client):
    result = client(GetDialogsRequest(
             offset_date=None,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=100,
             hash=0)) 

    entities = result.chats

    return entities


def read_messages(client, chats):

    # if chats == None :
    #     chats = ["iPapkornBots"]
    df = pd.DataFrame()
    for chat in chats:
        for message in client.iter_messages(chat, offset_date=datetime.date.today() + datetime.timedelta(days=-10) , reverse=True):
            # print(message)
            data = { "group" : chat, "sender" : message.sender_id, "text" : message.text, "date" : message.date}
            print(message.text)

            temp_df = pd.DataFrame(data, index=[1])
            df = df.append(temp_df)



def get_entity_data(client, entity_id, limit):
    entity = client.get_entity(entity_id)
    # today = datetime.datetime.today()
    posts = client(GetHistoryRequest(
                   peer=entity,
                   limit=limit,
                   offset_date=None,
                   offset_id=0,
                   max_id=0,
                   min_id=0,
                   add_offset=0,
                   hash=0))

    messages = []
    for message in posts.messages:
        messages.append(message.message)
    
    msg_df = pd.DataFrame(messages)
    msg_df.columns = ["raw_msg"]
    return msg_df