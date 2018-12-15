import random

import requests
import vk_api
from config import *


def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})


vk_bot = vk_api.VkApi(token=TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']
print("готов к работе")

 #+ str(long_poll))

def write_msg_attach(user_id, text, att_url):
    vk_bot.method('messages.send',
                  {'user_id': user_id,
                   'attachment': att_url,
                   'message': text,
                   'random_id': random.randint(0, 5000)})
def get_last_post(owner_id, count, offset, filter):
    response = vk_bot_user.method('wall_get',
                                  {'owner_id': owner_id,
                                   'count': count,
                                   'offset': offset,
                                   'filter': filter})

    return response['items'][0]['id']
#vk_bot_user = vk_api.VkApi(token=ACCESS_TOKEN)


while True:
 long_poll = requests.get(
        'https://{server}?act={act}&key={key}&ts={ts}&wait=15000'.format(server=server,
                                                                       act='a_check',
                                                                       key=key,
                                                                       ts=ts)).json()
 update = long_poll['updates']
 if update[0][0] == 4:
        print(update)
        user_id = update[0][3]
        user_name = vk_bot.method('users.get', {'user_ids': user_id})
        if 'привет' in update[0][6]:
            write_msg(user_id, 'здоров, ' + (user_name[0]['first_name']))  # cooбщение пользователю
        print(str(user_name[0]['first_name']) + ' ' +
              str(user_name[0]['last_name']) + ' написал(а) боту - ' + str(update[0][6]))  # cooбщение пользователя
        if 'красив' in update[0][6]:
            group_id = -35684707
            post_id = get_last_post(group_id, 1, 1, 'owner')
            attach = 'wall' + str(group_id) + '_' + str(post_id)
            write_msg_attach(user_id, 'держи', attach)
        elif 'домашка' in update[0][6]:
            write_msg_attach()
        elif 'матриц' in update[0][6]:
            write_msg_attach(user_id,
                             'Во имя чего, мистер Андерсен?',
                             'audio354852936_456239159')
        else: write_msg(user_id, 'кавуо')
    # меняем ts для след запроса
 ts = long_poll['ts']