import pandas as pd
from datetime import datetime
import requests
import calendar 
import telebot

class bCoin:

    #Первый скан
    first_scan = True

    # Конструктор
    def __init__(self, symbolName = '', timeFrame  = '60'):
        
        #Имя монеты (нпр BTCUSDT)
        self.SymbolName = symbolName

        #Текущая стоимость монеты
        self.CurrentPrice = 0.0

        #Стоимость монеты в предыдущем цикле
        self.OldPrice = 0.0

        #Текущий индекс RSIs
        self.CurrentRsi = 0.0

        #Индекс RSI в прошлом скане
        self.OldRsi = 0.0

        #Таймфрейм, мин
        self.TimeFrame = timeFrame

        self.delta_price = 0.0

        #Период для вычисления RSI
        self.RsiPeriod = 14

    # Метод для обновления показателей
    def Update(self):
        
        #Возвращаемое значение
        ret_value = ''

        try:
            now = datetime.utcnow()
            unixtime = calendar.timegm(now.utctimetuple())
            since = unixtime
            start = str(since - 60 * self.TimeFrame * (self.RsiPeriod + 1))    

            url = 'https://api.bybit.com/public/linear/kline?symbol=' + self.SymbolName + '&interval=' + str(self.TimeFrame) +'&from=' + str(start)  
            text = requests.get(url)
            
            data = text.json()
            #print(data)

            #Получение блоков с данными Candle
            D = pd.DataFrame(data['result'])
            

            #Copyright by Bitonegreat   www.bitonegreat.com
        
            df=D
            df['close'] = df['close'].astype(float)
            df2=df['close'].to_numpy()
            
            #Получение стоимости монеты
            self.CurrentPrice = df2[df2.size - 1]

            df2 = pd.DataFrame(df2, columns = ['close'])
            delta = df2.diff()
            
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            
            _gain = up.ewm(com = (self.RsiPeriod - 1), min_periods = self.RsiPeriod).mean()
            _loss = down.abs().ewm( com = (self.RsiPeriod - 1), min_periods = self.RsiPeriod).mean()
            
            RS = _gain / _loss

            
            
            self.CurrentRsi = 100 - (100 / (1 + RS))  
            self.CurrentRsi = self.CurrentRsi['close'].iloc[-1]
            self.CurrentRsi = round(self.CurrentRsi, 1)

            
            #Если это первый скан
            if self.first_scan == True:
                self.OldRsi = self.CurrentRsi
                self.OldPrice = self.CurrentPrice

            #Определение роста стоимости
            self.delta_price = round((self.CurrentPrice - self.OldPrice)/self.OldPrice * 100.0, 3)

            #Формирование сигнала на продажу монеты
            if self.OldRsi > 70 and self.CurrentRsi < 70:
                ret_value ='Пара: ' + self.SymbolName + '\n' + 'Стоимость: ' + str(self.CurrentPrice) + '\n' + 'RSI: ' + str(self.CurrentRsi) + '\n' + 'Таймфрейм: ' + str(self.TimeFrame) + '\n' + 'Сигнал для продажи'

            #Формирование сигнала на покупку монеты
            if self.OldRsi < 30 and self.CurrentRsi > 30:
                ret_value = ' Пара: ' + self.SymbolName + '\n' + 'Стоимость: ' + str(self.CurrentPrice) + '\n' + 'RSI: ' + str(self.CurrentRsi) + '\n' + 'Таймфрейм: ' + str(self.TimeFrame) + '\n' + 'Сигнал для покупки'
           

            #Вывод информации в консоль
            now = datetime.now()
            strtime = now.strftime("%Y.%m.%d  %H:%M:%S")
            
            debug_text = str(strtime) + ' Пара: ' + self.SymbolName + '\tСтоимость: ' + str(self.CurrentPrice) + '\tRSI: ' + str(self.CurrentRsi) + '\tИзменение стоимости: ' + str(self.delta_price)
            print(debug_text) 

            #Запоминание старого значения RSI
            self.OldRsi = self.CurrentRsi

            #Запоминание старого значения стоимости
            self.OldPrice = self.CurrentPrice


        except Exception as ex:
            print('\nExeption:  ', ex)

        #Сброс флага первого скана
        self.first_scan = False

        #Возврат значения
        return ret_value
