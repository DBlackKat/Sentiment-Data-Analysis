import pandas as pd
import numpy as np
import os
from math import floor
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return floor(val) / 10 ** digits

def convert_Dict_DF(df): #initial prototype convert dictionary data to dataframe function, see the below ones for current implementation
    margin1 = []
    margin2 = []
    margin3 = []
    sentiment = []
    idx = []
    for x in range(len(df['Buy'])):
        margin1.append(floored_percentage((df['1stDay'][x]-df['Buy'][x])/df['Buy'][x],3))
        margin2.append(floored_percentage((df['3rdDay'][x]-df['Buy'][x])/df['Buy'][x],3))
        margin3.append(floored_percentage((df['5thDay'][x]-df['Buy'][x])/df['Buy'][x],3))
        sentiment.append(float(df['sentiment'][x]))
        idx.append(x+1)
    d = {'1 day margin':pd.Series(margin1,index = idx),
         '3 day margin':pd.Series(margin2,index = idx),
         '5 day margin':pd.Series(margin3,index = idx),
         'Sentiment':pd.Series(sentiment,index = idx)}
    frame = pd.DataFrame(d)
    return frame

def convert_Dict_DF2(df):
    margin = [[],[],[],[],[],[],[]]
    sentiment = []
    idx = []
    for x in range(len(df['Buy'])):
        margin[0].append((df['1stDay'][x]-df['Buy'][x])/df['Buy'][x])
        margin[1].append((df['3rdDay'][x]-df['Buy'][x])/df['Buy'][x])
        margin[2].append((df['5thDay'][x]-df['Buy'][x])/df['Buy'][x])
        margin[3].append((df['7thDay'][x]-df['Buy'][x])/df['Buy'][x])
        margin[4].append((df['9thDay'][x]-df['Buy'][x])/df['Buy'][x])
        margin[5].append((df['13thDay'][x]-df['Buy'][x])/df['Buy'][x])
        margin[6].append((df['15thDay'][x]-df['Buy'][x])/df['Buy'][x])
        sentiment.append(float(df['sentiment'][x]))
        idx.append(x+1)

    d = {'1 day margin':pd.Series(margin[0],index = idx),
         '3 day margin':pd.Series(margin[1],index = idx),
         '5 day margin':pd.Series(margin[2],index = idx),
         '7 day margin':pd.Series(margin[3],index = idx),
         '9 day margin':pd.Series(margin[4],index = idx),
         '13 day margin':pd.Series(margin[5],index = idx),
         '15 day margin':pd.Series(margin[6],index = idx),
         'Sentiment':pd.Series(sentiment,index = idx)}
    frame = pd.DataFrame(d)
    return frame
def call_data(name_list):
    frames = []
    for x in name_list:
        pickle_path = os.path.join(os.getcwd(),'results/'+x+'_F.p')
        read = pd.read_pickle(pickle_path)
        df = convert_Dict_DF2(read)
        frames.append(df)

    result = pd.concat(frames)
    return (result/100)

if __name__ == '__main__':
    # name = 'INTEL_CORP'
    tick_Name = ['TESLA','FACEBOOK','APPLE_INC','EXXON_MOBIL','JPMORGAN','BANK_OF_AMERICA','GENERAL_MOTOR','AMAZON','MICROSOFT','INTEL_CORP','ABBOTT_LABORATORIES','ALLERGAN_INC','MONSANTO_CO','SYNGENTA_AG','YAHOO_INC','3M_CO','CATERPILLAR_INC','EBAY_INC','GENERAL_ELECTRIC_CO','MASTER_CARD']
    # pickle_path = os.path.join(os.getcwd(),'results/'+tick_Name[0]+'_F.p')
    # read = pd.read_pickle(pickle_path)
    #df = convert_Dict_DF2(read)

    frame = call_data(tick_Name)
    logReturn = np.log(frame+1)
    sns.plt.xlim(-0.006, 0.006)
    sns.plt.subplot(7,1,1)
    a1 = sns.regplot(x="1 day margin", y="Sentiment", data=logReturn,ci=None,color="#1dad9b")
    sns.plt.subplot(7,1,2)
    a2 = sns.regplot(x="3 day margin", y="Sentiment", data=logReturn,ci=None,color="#41B3D3")
    sns.plt.subplot(7,1,3)
    a3 = sns.regplot(x="5 day margin", y="Sentiment", data=logReturn,ci=None,color="#11999e")
    sns.plt.subplot(7,1,4)
    a4 = sns.regplot(x="7 day margin", y="Sentiment", data=logReturn,ci=None,color="#41B3D3")
    sns.plt.subplot(7,1,5)
    a5 = sns.regplot(x="9 day margin", y="Sentiment", data=logReturn,ci=None,color="#1dad9b")
    sns.plt.subplot(7,1,6)
    a6 = sns.regplot(x="13 day margin", y="Sentiment", data=logReturn,ci=None,color="#11999e")
    sns.plt.subplot(7,1,7)
    a7 = sns.regplot(x="15 day margin", y="Sentiment", data=logReturn,ci=None,color="#1dad9b")
    sns.plt.show()


    C1 = frame['1 day margin'].corr(frame['Sentiment'])
    C2 = frame['3 day margin'].corr(frame['Sentiment'])
    C3 = frame['5 day margin'].corr(frame['Sentiment'])
    c1 = np.correlate(frame['Sentiment'],frame['1 day margin'])
    c2 = np.correlate(frame['Sentiment'],frame['3 day margin'])

    print "1Day correlation: {}".format(C1)
    print "3Day correlation: {}".format(C2)
    print "5Day correlation: {}".format(C3)
    for x in range(8):
        if (2*x+1) == 11:
            continue
        string =str(2*x+1)+' day margin'
        x = frame[string].values
        y = frame['Sentiment'].values
        X = []
        Y = []
        for i in range(len(x)):
            if not np.isnan(x[i]) or np.isnan(y[i]):
                X.append(x[i])
                Y.append(y[i])
        slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
        print string
        print 'slope = {}, intercept= {}, r_value={}, p_value={}, std_err={}'.format(slope, intercept, r_value, p_value, std_err)
        C1 = frame[string].corr(frame['Sentiment'])
        print string +" correlation with sentiment : {}\n".format(C1)
