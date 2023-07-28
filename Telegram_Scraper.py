import configparser
import json
import asyncio
from datetime import date, datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
# config = configparser.ConfigParser()
# config.read("config-sample2.ini")

# Setting configuration values
#Enter your credentials here
api_id = #your api id here
api_hash = 'your api hash here'

api_hash = str(api_hash)

phone = #your phone number here
username = 'yourusernamehere'

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)


def telegram_scrape(link, file_name, phone= #yourphonehere):
    async def main(phone):
        await client.start()
        print("Client Created")
        # Ensure you're authorized
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        me = await client.get_me()

        user_input_channel = link

        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await client.get_entity(entity)

        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = await client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        with open(file_name, 'w') as outfile:
            json.dump(all_messages, outfile, cls=DateTimeEncoder)

    with client:
        client.loop.run_until_complete(main(phone))


# Fill channel_list with the URLs of channels you wish to scrape

channel_list = ['https://t.me/truexanewsua','https://t.me/yurasumy', 'https://t.me/u_now',
                'https://t.me/voynareal', 'https://t.me/insiderUKR', 'https://t.me/UaOnlii',
                'https://t.me/oko_ua1', 'https://t.me/lachentyt', 'https://t.me/+4kAkN49IKJBhZDk6',
                'https://t.me/+U3r_kPBc7PpgiYP7', 'https://t.me/+V8VPwRkVmO9mODBi', 'https://t.me/ASupersharij',
                'https://t.me/V_Zelenskiy_official', 'https://t.me/TCH_channel', 'https://t.me/kievreal1',
                'https://t.me/legitimniy', 'https://t.me/bozhejakekonchene', 'https://t.me/rezident_ua',
                'https://t.me/UkraineNow', 'https://t.me/ukraina_novosti', 'https://t.me/+aAaZ8kQkkpo2ZjRi',
                'https://t.me/mykolaivskaODA', 'https://t.me/xydessa', 'https://t.me/alarmukraine',
                'https://t.me/+_osZLpRD48c3ODYy', 'https://t.me/+gFCT63NlnfE5YWZi',  'https://t.me/+3sUd12FqwxliYWY6',
                'https://t.me/RKadyrov_95', 'https://t.me/novosti_voinaa', 'https://t.me/rian_ru',
                'https://t.me/leoday', 'https://t.me/+AzFt2ITq9hg3ZjQy', 'https://t.me/+B4-55MTTqXs0MzEy',
                'https://t.me/breakingmash', 'https://t.me/readovkanews', 'https://t.me/+GvivdThlMX1jZjRi',
                'https://t.me/kino_hd2', 'https://t.me/+7W2WZ9ZFhapmMTRi', 'https://t.me/bbbreaking',
                'https://t.me/ostorozhno_novosti', 'https://t.me/+_e4kuJNgtuphZTFi', 'https://t.me/SolovievLive',
                'https://t.me/litvintm', 'https://t.me/wargonzo', 'https://t.me/moscowmap',
                'https://t.me/bloodysx', 'https://t.me/meduzalive', 'https://t.me/maslennikovliga',
                'https://t.me/topor', 'https://t.me/RVvoenkor']




for i in range(len(channel_list)):
    file_name = f'extra_channel_message_{i}.json'
    try:
        telegram_scrape(channel_list[i], file_name)
    except:
        print(f'Failure at URL{i}')
