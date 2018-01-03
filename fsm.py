from transitions.extensions import GraphMachine

from random import *
import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import os



class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
################################################################
    def is_going_to_listen1(self, update):
        print('go to search Summoner')
        text = update.message.text
        return text.lower() == 'search my rank'

    def on_enter_listen1(self, update):
        update.message.reply_text("Please Enter Summoner's Name ")

    def on_exit_listen1(self, update):
        print('Leaving state1')


    def is_going_to_rank(self, update):
        print('going to rank')
        text = update.message.text
        Rank=crawler_rank(text)
        if Rank!='Wrong Input Name!!':
           update.message.reply_text("Rank:")
           update.message.reply_text(Rank)
           return True
        else:
           update.message.reply_text('Wrong Input')
           return False
          

    def on_enter_rank(self, update):
        print('on enter')
	
    def on_exit_rank(self, update):
        print('Leaving rank')


    def is_going_to_stat(self, update):
        print('going to rank')
        text = update.message.text
        Stat=crawler_record(text)
        if Stat!='Wrong Input Name!!':
           update.message.reply_text("狀態:")
           update.message.reply_text(Stat)
           return True
        else:
           update.message.reply_text('Wrong Input')
           return False


    def on_enter_stat(self, update):
        print('on enter stat')
        self.go_back(update)


    def on_exit_rank(self, update):
        print('Leaving stat')
###############################################################
    def is_going_to_listen2(self, update):
        print('go to search hero')
        text = update.message.text
        return text.lower() == 'search pop hero'

    def on_enter_listen2(self, update):
        update.message.reply_text("請選取何種牌位和哪個位置")
        update.message.reply_text("位置 上路:/top 中路:/middle 打野:/jungle AD:/adc 輔助:/support")	
        update.message.reply_text("牌位 全部:/all 青銅:/bronze 白銀:/silver 黃金:/gold 白金:/platinum 鑽石:/diamond")
        update.message.reply_text("牌位和位置都可選可不選 範例: /top/silver or /top or /bronze")

    def on_exit_listen2(self, update):
        print('Leaving state2')


    def is_going_to_hero(self, update):
        print('going to hero')
        text = update.message.text
        Hero=crawler_hero(text)
        if Hero!='Wrong Input':
           update.message.reply_text("Top 5 Hero:")
           update.message.reply_text(Hero)
           return True
        else:
           update.message.reply_text('Wrong Input')
           return False

    def on_enter_hero(self, update):
        print('on enter')
        self.go_back(update)

    def on_exit_hero(self, update):
        print('Leaving Hero')
#################################################################
    def is_going_to_time(self, update):
        print('going to time')
        text = update.message.text
        return text.lower() == 'search game average time'

    def on_enter_time(self, update):
        print('on enter')
        Time=crawler_time()
        update.message.reply_text("平均遊戲時間:")
        update.message.reply_text(Time)
        self.go_back(update)
	
    def on_exit_time(self, update):
        print('Leaving time')

##################################################################
def crawler_rank(name='ScorpioGary'):
    url="https://lol.moa.tw/summoner/show/"+name
    print('Your want to search '+name)
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    articles=soup.select('div.col-xs-6')
    if len(articles)==0:
        rank=("Wrong Input Name!!")
    else:
        rank=articles[0].text
    print(rank)
    return rank
###################################################################
def crawler_hero(state):
    url='https://www.leagueofgraphs.com/zh/champions/stats'
    #state='/top/silver'
    url=url+state
    print(url)
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    articles=soup.select('table.data_table')
    if len(articles)==0:
        print("Wrong Input")
        result=("Wrong Input")
        return result
    article=articles[0]


    rows=article.findAll('tr')
    data=[]
    i=0
    for row in rows:
        i=i+1
        cols=row.findAll("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
        if i>=6:
            break
    del data[0]
    result="   名子      出場率 勝率 禁用率 K/D/A  場均五連殺\n"
    for row in range(5):
        tmp=''
        for col in range(7):
            data[row][col]=data[row][col].replace(' ','')
            data[row][col]=data[row][col].replace('\n','')
            data[row][col]=data[row][col].replace('\r','')
            if col>=2 and col<=4:
                if col==4:
                   data[row][col]=data[row][col][:4]
                else:
                   data[row][col]=data[row][col][:5]
            tmp=tmp+data[row][col]+' '
        tmp=tmp+"\n"
        result=result+tmp
                   
    print(result)           
    return result
###########################################################################
def crawler_time():
    url="https://www.leagueofgraphs.com/zh/rankings/game-durations"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    articles=soup.select('table.data_table.sortable_table')
    article=articles[0]
    
    rows=article.findAll('tr')
    data=[]
    for row in rows:
        cols=row.findAll("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    del data[0]

    result=''
    for row in range(len(data)):
        tmp=''
        for col in range(len(data[0])):
            data[row][col]=data[row][col].replace(' ','')
            data[row][col]=data[row][col].replace('\n','')
            data[row][col]=data[row][col].replace('\r','')
            if col==1:
                data[row][col]=data[row][col][:5]
            tmp=tmp+data[row][col]+'    '
        tmp=tmp+'\n'
        result=result+tmp
            
    print(result)
    return result
#####################################################################
def crawler_record(name='ScorpioGary'):
    url="https://lol.moa.tw/summoner/show/"+name
    print('Your want to search '+name)
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    articles=soup.select('div.col-xs-3.h2')
    if len(articles)==0:
        data=("Wrong Input Name!!")
        return data
    result=''
    result="友善:      "+articles[0].text+'\n'
    result=result+"熱心助人:  "+articles[1].text+'\n'
    result=result+"團隊合作:  "+articles[2].text+'\n'
    result=result+"可敬的對手:"+articles[3].text+'\n'
    print(result)
    return result 
