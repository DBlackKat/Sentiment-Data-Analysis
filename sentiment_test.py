import pandas as pd
import numpy as np
import os,pickle

def load_Data(name):
    pickle_path = os.path.join(os.getcwd(),'database/'+name+'.p')
    df = pd.read_pickle(pickle_path)
    return df
def load_Sentiment(name):
    pickle_path = os.path.join(os.getcwd(),'sentiment/'+name+'_NS1.p')
    df = pd.read_pickle(pickle_path)
    return df

def pastSentimentCompare(name):
    df = load_Data(name)
    sen = load_Sentiment(name)
    analysis = dict()
    buy = []
    tradingVol = []
    pastDay = [[],[],[],[],[],[],[]]
    Day = [[],[],[],[],[],[],[]]
    news_Vol = []
    news_Buzz = []
    senti = []
    date = []
    print "reading {}....".format(name)
    for y in range(len(sen)):
        if(sen['Sentiment Low'].values[y] != 0 ) and (sen['Sentiment High'].values[y] != 0 ) and (sen['News Volume'].values[y] != 0 ):
            for x in range(len(df)):
                if df.index[x] == sen.index[y]:
                    date.append(sen.index[y])
                    buy.append(df['Open'].values[x])
                    tradingVol.append(df['Volume'].values[x])
                    for i in range(7):
                        if((x+1+i) < len(df)):
                            Day[i].append(df['Close'].values[x+1+i])
                        else:
                            Day[i].append(np.nan)
                    for j in range(-7,0):
                        if((x+j) > 0):
                            pastDay[j].append(df['Close'].values[x+j])
                        else:
                            pastDay[j].append(np.nan)
                    senti.append(sen['Sentiment'].values[y])
                    news_Buzz.append(sen['News Buzz'].values[y])
                    news_Vol.append(sen['News Volume'].values[y])

    analysis['Buy']=buy
    analysis['tradingVol'] = tradingVol
    analysis['1stDay']=Day[0]
    analysis['2ndDay']=Day[1]
    analysis['3rdDay']=Day[2]
    analysis['4thDay']=Day[3]
    analysis['5thDay']=Day[4]
    analysis['6thDay']=Day[5]
    analysis['7thDay']=Day[6]
    for i in range(7):
        name = '-'+str(i+1)+'th'+'Day'
        analysis[name] = pastDay[i]
    analysis['sentiment'] = senti
    analysis['NewsVol'] = news_Vol
    analysis['NewsBuz'] = news_Buzz
    analysis['date'] = date

    return analysis


# def relate_SentimentNPrice(name):
#     df = load_Data(name)
#     sen = load_Sentiment(name)
#     analysis = dict()
#     buy = []
#     Day = [[],[],[],[],[],[],[]]
#     news_Vol = []
#     news_Buzz = []
#     senti = []
#     date = []
#     print "reading {}....".format(name)
#     for y in range(len(sen)):
#         if(sen['Sentiment Low'].values[y] != 0 ) and (sen['Sentiment High'].values[y] != 0 ) and (sen['News Volume'].values[y] != 0 ) :
#             for x in range(len(df)):
#                 if df.index[x] == sen.index[y]:
#                     date.append(sen.index[y])
#                     buy.append(df['Open'].values[x])
#                     for i in range(7):
#                         if((x+1+i*2) < len(df)):
#                             Day[i].append(df['Open'].values[x+1+i])
#                         else:
#                             Day[i].append(np.nan)
#                     senti.append(sen['Sentiment'].values[y])
#                     news_Buzz.append(sen['News Buzz'].values[y])
#                     news_Vol.append(sen['News Volume'].values[y])
#
#     analysis['Buy']=buy
#     analysis['1stDay']=Day[0]
#     analysis['3rdDay']=Day[1]
#     analysis['5thDay']=Day[2]
#     analysis['7thDay']=Day[3]
#     analysis['9thDay']=Day[4]
#     analysis['13thDay']=Day[5]
#     analysis['15thDay']=Day[6]
#     analysis['sentiment'] = senti
#     analysis['NewsVol'] = news_Vol
#     analysis['NewsBuz'] = news_Buzz
#     analysis['date'] = date
#     return analysis

def generate_result(tick_Name):
    outDir = os.path.join( os.getcwd(),'resultsMKII') # dir for all inputs and outputs
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    for name in tick_Name:
        analysis = pastSentimentCompare(name)
        pickle_path = os.path.join(os.getcwd(),'resultsMKII/'+name+'_F.p')
        pickle.dump(analysis,open(pickle_path,'wb'))
        print "finish {}...".format(name)

if __name__ == '__main__':
    tick_Name = ['TESLA','FACEBOOK','APPLE_INC','EXXON_MOBIL','JPMORGAN','BANK_OF_AMERICA','GENERAL_MOTOR','AMAZON','MICROSOFT','INTEL_CORP','ABBOTT_LABORATORIES','ALLERGAN_INC','MONSANTO_CO','SYNGENTA_AG','YAHOO_INC','3M_CO','CATERPILLAR_INC','EBAY_INC','GENERAL_ELECTRIC_CO','MASTER_CARD']
    generate_result(tick_Name)