import seaborn as sns
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

def relate_SentimentNPrice(name):
    df = load_Data(name)
    sen = load_Sentiment(name)
    df = df[sen[0:1].index[0]:]
    analysis = dict()
    buy = []
    firstDay = []
    thirdDay = []
    fithDay = []
    news_Vol = []
    news_Buzz = []
    senti = []
    date = []
    print "reading {}....".format(name)
    for y in range(len(sen)):
        if(sen[y:y+1]['Sentiment Low'].values != 0 ) and (sen[y:y+1]['Sentiment High'].values != 0 ) and (sen[y:y+1]['News Volume'].values != 0 ) :
            for x in range(len(df)):
                if df[x:x+1].index[0] == sen[y:y+1].index[0]:
                        date.append(sen[y:y+1].index[0])
                        buy.append(df[x:x+1]['Open'].values[0])
                        if(x+2 < len(df)):
                            firstDay.append(df[x+1:x+2]['Open'].values[0])
                        else:
                            firstDay.append(np.nan)
                        if x+5<len(df):
                            thirdDay.append(df[x+4:x+5]['Open'].values[0])
                        else:
                            thirdDay.append(np.nan)
                        if x+7 < len(df):
                            fithDay.append(df[x+6:x+7]['Open'].values[0])
                        else:
                            fithDay.append(np.nan)
                        senti.append(sen[y:y+1]['Sentiment'].values[0])
                        news_Buzz.append(sen[y:y+1]['News Buzz'].values[0])
                        news_Vol.append(sen[y:y+1]['News Volume'].values[0])

    analysis['Buy']=buy
    analysis['1stDay']=firstDay
    analysis['3rdDay']=thirdDay
    analysis['5thDay']=fithDay
    analysis['sentiment'] = senti
    analysis['NewsVol'] = news_Vol
    analysis['NewsBuz'] = news_Buzz
    analysis['date'] = date
    return analysis
def generate_result(tick_Name):
    outDir = os.path.join( os.getcwd(),'results') # dir for all inputs and outputs
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for name in tick_Name[0:len(tick_Name)]:
        analysis = relate_SentimentNPrice(name)
        pickle_path = os.path.join(os.getcwd(),'results/'+name+'_NS1.p')
        pickle.dump(analysis,open(pickle_path,'wb'))
        print "finish {}...".format(name)

if __name__ == '__main__':
    tick_Name = ['TESLA','FACEBOOK','APPLE_INC','EXXON_MOBIL','JPMORGAN','BANK_OF_AMERICA','GENERAL_MOTOR','AMAZON','MICROSOFT','INTEL_CORP']
    generate_result(tick_Name)