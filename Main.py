import pandas as pd
import time
import requests
import telebot
from datetime import datetime
import calendar 

import bCoin


#Список монет для контроля
bCoinslist = [
              bCoin.bCoin('BTCUSDT',  60),
              bCoin.bCoin('ETHUSDT',  60),  
              bCoin.bCoin('SOLUSDT',  60), 
              bCoin.bCoin('ADAUSDT',  60),  
              bCoin.bCoin('DOTUSDT',  60), 
              bCoin.bCoin('AVAXUSDT', 60),  
              bCoin.bCoin('DOGEUSDT', 60)]

chat_id=426440018
bot_token = '1562305259:AAEnmudwYvRuzNlIq1XoUJtoL4iqkEcS-wg'

bot = telebot.TeleBot(bot_token)


#Отладочная информация для вывода в консоль
debug_text ='\n\n##########################################################################################################'
print(debug_text)

while True:

    for bCoin in bCoinslist:
        msg = bCoin.Update()

        if len(msg) > 0:
            bot.send_message(chat_id, text=msg)

        #Задерка 60 сек
        time.sleep(60)
