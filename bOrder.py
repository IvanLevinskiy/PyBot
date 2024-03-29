import telebot

#Класс описывает сущность ордера
#на покупку монеты с предоставлением статистики
class bOrder:

    

    # Конструктор
    def __init__(self, telegrammBot, bCoin, entryPrice = 0.0):
        
         #Передача указателя на монету
        self.BCoin = bCoin

        #Стоимость монеты при входе
        self.EntryPrice = entryPrice

        #Передача указателя на телеграмм бота
        self.telegrammBot = telegrammBot

        #ID чата
        self.chat_id = 426440018

        msg = 'Пара: ' + self.BCoin.SymbolName + '\n' + 'Стоимость: ' + str(self.BCoin.CurrentPrice) + '\n' + 'RSI: ' + str(self.BCoin.CurrentRsi) + '\n' + 'Таймфрейм: ' + str(self.BCoin.TimeFrame) + '\n' + 'Сигнал для покупки'

        self.telegrammBot.send_message(self.chat_id, text = msg)



    # Метод для завершения ордера и вывода 
    #информации в телеграмм бота о статистики ордера
    def Close(self, exitPrice = 0.0):
        
        profit = (exitPrice - self.EntryPrice)/ self.EntryPrice * 100.0
        profit = round(profit, 1)

        msg = 'Пара: ' + self.BCoin.SymbolName + '\n' + 'Стоимость: ' + str(self.BCoin.CurrentPrice) + '\n' + 'RSI: ' + str(self.BCoin.CurrentRsi) + '\n' + 'Таймфрейм: ' + str(self.BCoin.TimeFrame) + '\n' + 'Профит: ' + str(profit) + '\n' + 'Сигнал для продажи'
        self.telegrammBot.send_message(self.chat_id, text = msg)
