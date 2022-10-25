import random, vk_api
import vk
import requests
import sqlite3
from dpath.util import values as path_val
from vk_api.utils import get_random_id
vk_session = vk_api.VkApi(token='4bb313f0a86f83dab0e938175d2e0dce6247ffbf1f6f9fbb33410d3a077d47e71fa74712a5188cbb44437')
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from yahooparser import Ticker
#import os
#import sys
import datetime
import time
from random import randint
#import threading
#from threading import Thread
from datetime import datetime, timezone, timedelta
#longpoll = VkBotLongPoll(vk_session, 212774888)
vk = vk_session.get_api()
#from vk_api.longpoll import VkLongPoll, VkEventType
#version 1.07.0
#Lslongpoll = VkLongPoll(vk_session)
#Lsvk = vk_session.get_api()
job = False
tzinfo = timezone(timedelta(hours=3))
our_chat_id = 1
def send_message(message, event):
	if event.from_chat:
	    vk.messages.send(
			random_id = get_random_id(),
			message=message,
			chat_id = event.chat_id,
			our_chat_id = event.chat_id
			)
	elif event.from_user:
	    vk.messages.send(
			peer_id = event.message.peer_id,
			message = message,
			random_id = get_random_id()
  				)
def send_message_our_chat(message, chat_id):
    vk.messages.send(
		random_id = get_random_id(),
		message=message,
		chat_id = chat_id
		)
def countrang():
    global cur
    count = 0
    cur.execute("Select count(rang) from rangs")
    for row in cur.fetchall():
        count = int(row[0])
    return count
def addrang(event, rang):
    global cur
    global con
    count = countrang()
    cur.execute("INSERT INTO Rangs(id, rang) VALUES ('"+ str(count) + "', '" + rang + "');")
    con.commit()
    print(noew() + ": Титул " + rang + " записан.")
    send_message('Титул добавлен', event)
def viewrangs(event):
    global cur
    count = countrang()
    rangs = "Титулы на " + noew() + ". Всего " + str(count) + " титулов:"
    cur.execute("SELECT rang FROM rangs")
    for row in cur.fetchall():
        rangs = rangs + "\n" + row[0]
    send_message(rangs, event)
    print(noew() + ": Титулы показаны.")
def removerang(event):
    global cur
    global con
    count = countrang()
    cur.execute("DELETE FROM rangs WHERE id='" + str(count - 1) + "';")
    con.commit()
    print(noew() + ": Титул удалён.")
    send_message('Титул удалён', event)
def who(event, whois):
    random_user = randint(0, len(vk.messages.getConversationMembers(peer_id = 2000000000 + event.chat_id)['profiles']) - 1)
    random_user_id = vk.messages.getConversationMembers(peer_id = 2000000000 + event.chat_id)['profiles'][random_user]['id']
    send_message("Я думаю, что " + get_name(random_user_id) + " " + whois, event)
    #send_message("k_api.exceptions.ApiError: [917] You don't have access to this chat", event)
def get_name(user_id):
    name = vk.users.get(user_ids=(user_id))[0]['first_name'] + " " + vk.users.get(user_ids=(user_id))[0]['last_name']
    return name
def noew():
    return datetime.now(tzinfo).strftime("%d.%m.%Y %H:%M:%S")
def viewrangs_sort(event):
    global cur
    count = countrang()
    rangs = "Титулы на " + noew() + ". Всего " + str(count) + " титулов:"
    cur.execute("SELECT rang FROM rangs ORDER BY rang")
    for row in cur.fetchall():
        rangs = rangs + "\n" + row[0]
    send_message(rangs, event)
    print(noew() + ": Титулы показаны.")
def be_rang(event, rang):
    global cur
    count = 0
    cur.execute("SELECT COUNT(rang) FROM rangs WHERE rang = '" + rang + "'")
    for row in cur.fetchall():
        count = int(row[0])
    if count > 0:
        send_message('Уже был', event)
    else:
        send_message('Такого титула ещё не было', event)
def stonks(name, event):
    try:
        ticker = Ticker(name)
        ticker.update()
        price = round(ticker.price, 2)
        change = round(ticker.change, 2)
        percent = round(ticker.percent * 100, 2)
        volume = round(ticker.volume, 2)
        send_message("Акции " + name + " стоят " + str(price) + "р. Изменение: " + str(change) + "р (" + str(percent) + "%). Объём торгов: " + str(volume) + " штук.", event)
    except Exception:
        send_message('Мне такие неизвестны', event)
def govno(event):
    f = open('/home/Kozzlv/bot/Govno.txt','r')
    govno = f.readline().split(";")
    f.close()
    dt = (datetime.now(tzinfo) - datetime.strptime(govno[3], "%d.%m.%Y %H:%M:%S").replace(tzinfo=tzinfo)).total_seconds()/3600
    percent = float(govno[1])
    if dt > 1:
        percent = random.uniform(-0.0301, 0.0505)
        govno[0] = str(round(float(govno[0]) + float(govno[0])*percent, 2))
        govno[1] = str(round(percent, 2))
        govno[2] = str(round((float(govno[2]) + float(govno[2])*random.uniform(-0.01, 0.02)))) + ".0"
        govno[3] = str(noew())
        f = open('/home/Kozzlv/bot/Govno.txt','w')
        f.write(govno[0] + ";" + govno[1] + ";" + govno[2] + ";" + govno[3])
        f.close()
    send_message("Акции Говно стоят " + govno[0] + "р. Изменение: " + str(round(float(govno[0])*percent,4)) + "р (" + govno[1] + "%). Объём торгов: " + govno[2] + " штук.", event)
def listen():
    longpoll = VkBotLongPoll(vk_session, 212774888)
    global job
    global con
    global cur
    while job == True:
        print(noew() + ": Бот работает.")
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and len(event.message.text) >= 3:
                    print(get_name(event.message['from_id']) + " написал: " + event.message.text)
                    if event.message.text == "Бот" or event.message.text == "бот":
                        send_message('Ебал тебя в рот', event)
                    elif event.message.text == "Кто бот" or event.message.text == "кто бот":
                        send_message('Я', event)
                    elif event.message.text == "Кто сосал" or event.message.text == "кто сосал":
                        send_message('Тот, кто сказал 300', event)
                    elif event.message.text == "Хуй" or event.message.text == "хуй":
                        send_message('Ты хуй', event)
                    elif event.message.text == "Блять" or event.message.text == "блять" or event.message.text == "Блядь" or event.message.text == "блядь":
                        send_message('Надо дома оставлять', event)
                    elif event.message.text == "Остановить" or event.message.text == "остановить":
                        send_message('Останавливаюсь...', event)
                        job = False
                        return
                    elif event.message.text == "Перезапустить" or event.message.text == "перезапустить":
                        send_message('Перезапускаюсь...', event)
                        print(noew() + ": Перезапуск...")
                        return
                    elif "+Ранг " in event.message.text:
                        rang = event.message.text.replace("+Ранг ", "")
                        addrang(event, rang)
                    elif "+ранг " in event.message.text:
                        rang = event.message.text.replace("+ранг ", "")
                        addrang(event, rang)
                    elif "+Титул " in event.message.text:
                        rang = event.message.text.replace("+Титул ", "")
                        addrang(event, rang)
                    elif "+титул " in event.message.text:
                        rang = event.message.text.replace("+титул ", "")
                        addrang(event, rang)
                    elif event.message.text == "Ранги по алфавиту" or event.message.text == "ранги по алфавиту" or event.message.text == "Титулы по алфавиту" or event.message.text == "титулы по алфавиту":
                        viewrangs_sort(event)
                    elif event.message.text == "Ранги" or event.message.text == "ранги" or event.message.text == "Звания" or event.message.text == "звания" or event.message.text == "Писка рангов" or event.message.text == "писка рангов" or event.message.text == "Титулы" or event.message.text == "титулы":
                        viewrangs(event)
                    elif event.message.text == "Не нравится" or event.message.text == "не нравится":
                        removerang(event)
                    elif event.message.text == "Да" or event.message.text == "да":
                        send_message('Пизда', event)
                    elif event.message.text == "Нет" or event.message.text == "нет":
                        send_message('Пидора ответ', event)
                    elif event.message.text == "Кто я" or event.message.text == "кто я" or event.message.text == "Кто я?" or event.message.text == "кто я?":
                        send_message('Ты пидор', event)
                    elif len(event.message.text) >= 4 and event.message.text[0] == "К" and event.message.text[1] == "т" and event.message.text[2] == "о" and event.message.text[3] == " ":
                        whois = event.message.text.replace("Кто ", "")
                        who(event, whois)
                    elif len(event.message.text) >= 4 and event.message.text[0] == "к" and event.message.text[1] == "т" and event.message.text[2] == "о" and event.message.text[3] == " ":
                        whois = event.message.text.replace("кто ", "")
                        who(event, whois)
                    elif "Был ли ранг " in event.message.text:
                        whois = event.message.text.replace("Был ли ранг ", "")
                        whois = whois.replace("?", "")
                        be_rang(event, whois)
                    elif "был ли ранг " in event.message.text:
                        whois = event.message.text.replace("Был ли ранг ", "")
                        whois = whois.replace("?", "")
                        be_rang(event, whois)
                    elif event.message.text == "Акции GOVNO.ME" or event.message.text == "акции GOVNO.ME":
                        govno(event)
                    elif len(event.message.text) >= 6 and event.message.text[0] == "А" and event.message.text[1] == "к" and event.message.text[2] == "ц" and event.message.text[3] == "и" and event.message.text[4] == "и" and event.message.text[5] == " ":
                        name_stonks = event.message.text.replace("Акции ", "")
                        stonks(name_stonks, event)
                    elif len(event.message.text) >= 6 and event.message.text[0] == "а" and event.message.text[1] == "к" and event.message.text[2] == "ц" and event.message.text[3] == "и" and event.message.text[4] == "и" and event.message.text[5] == " ":
                        name_stonks = event.message.text.replace("акции ", "")
                        stonks(name_stonks, event)
        except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
            print("\n " + noew() + ": Переподключение к серверам ВК \n")
            time.sleep(3)
#ОСНОВНАЯ ПРОГРАММА
job = True
con = sqlite3.connect("Rangs.db")
cur = con.cursor()
listen()
con.close()