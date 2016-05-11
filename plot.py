import pandas as pd
import numpy as np
import os,pickle
from math import floor
import seaborn as sns
from scipy import stats
from scipy.stats import kendalltau
import matplotlib.pyplot as plt


def getLogReturn(df):
    margin = [[],[],[],[],[],[],[]]
    sentiment = []
    idx = []
    for x in range(len(df['Buy'])):
        margin[0].append(np.log((df['1stDay'][x])/df['Buy'][x]))
        margin[1].append(np.log((df['2ndDay'][x])/df['Buy'][x]))
        margin[2].append(np.log((df['3rdDay'][x])/df['Buy'][x]))
        margin[3].append(np.log((df['4thDay'][x])/df['Buy'][x]))
        margin[4].append(np.log((df['5thDay'][x])/df['Buy'][x]))
        margin[5].append(np.log((df['6thDay'][x])/df['Buy'][x]))
        margin[6].append(np.log(df['7thDay'][x]/df['Buy'][x]))
        sentiment.append(float(df['sentiment'][x]))
        idx.append(x+1)

    d = {'1 day':pd.Series(margin[0],index = idx),
         '2 day':pd.Series(margin[1],index = idx),
         '3 day':pd.Series(margin[2],index = idx),
         '4 day':pd.Series(margin[3],index = idx),
         '5 day':pd.Series(margin[4],index = idx),
         '6 day':pd.Series(margin[5],index = idx),
         '7 day':pd.Series(margin[6],index = idx),
         'Sentiment':pd.Series(sentiment,index = idx)}
    history = [[],[],[],[],[],[],[]]
    index = []
    for x in range(len(df['Buy'])):
        for i in range(7):
            name = '-'+str(i+1)+'th'+'Day'
            history[i].append(np.log((df[name][x])/df['Buy'][x]))
        index.append(x+1)

    for i in range(7):
        name = '-'+str(i+1)+' day'
        d[name] = pd.Series(history[i],index = index)
    frame = pd.DataFrame(d)
    return frame


def call_data(name_list,path):
    frames = []
    for x in name_list:
        pickle_path = os.path.join(os.getcwd(),path+'/'+x+'_F.p')
        read = pd.read_pickle(pickle_path)
        df = getLogReturn(read)
        frames.append(df)
    result = pd.concat(frames)
    pickle_path = os.path.join(os.getcwd(),'endResult_.p')
    pickle.dump(result,open(pickle_path,'wb'))
    return (result)

def getNewsNTradingVol(name_list,path):
    frames = []
    for x in name_list:
        pickle_path = os.path.join(os.getcwd(),path+'/'+x+'_F.p')
        read = pd.read_pickle(pickle_path)
        frames.append(pd.DataFrame(read))
    end = pd.concat(frames)
    return end

def plotSentimenAndTime(tickName):
    path2 = 'resultsMKII'
    frame2 = call_data(tick_Name,path2)
    # pickle_path = os.path.join(os.getcwd(),'endResult_.p')
    # frame2 = pd.read_pickle(pickle_path)

    sns.plt.xlim(-0.006, 0.006)
    sns.plt.subplot(3,1,1)
    a1 = sns.regplot(x="1 day", y="Sentiment", data=frame2,ci=None,color="#1dad9b")
    a1.set(xlabel= "Day 1 log return",ylabel="Sentiment")
    sns.plt.subplot(3,1,2)
    a2 = sns.regplot(x="2 day", y="Sentiment", data=frame2,ci=None,color="#41B3D3")
    a2.set(xlabel= "Day 2 log return",ylabel="Sentiment")
    sns.plt.subplot(3,1,3)
    a3 = sns.regplot(x="3 day", y="Sentiment", data=frame2,ci=None,color="#11999e")
    a3.set(xlabel= "Day 3 log return",ylabel="Sentiment")
    sns.plt.show()
    sns.plt.subplot(4,1,1)
    sns.plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,hspace = 0.5 )
    a4 = sns.regplot(x="4 day", y="Sentiment", data=frame2,ci=None,color="#41B3D3")
    a4.set(xlabel= "Day 4 log return",ylabel="Sentiment")
    sns.plt.subplot(4,1,2)
    sns.plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,hspace = 0.5 )
    a5 = sns.regplot(x="5 day", y="Sentiment", data=frame2,ci=None,color="#1dad9b")
    a5.set(xlabel= "Day 5 log return",ylabel="Sentiment")
    sns.plt.subplot(4,1,3)
    sns.plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,hspace = 0.5)
    a6 = sns.regplot(x="6 day", y="Sentiment", data=frame2,ci=None,color="#11999e")
    a6.set(xlabel= "Day 6 log return",ylabel="Sentiment")
    sns.plt.subplot(4,1,4)
    sns.plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,hspace = 0.5)
    a7 = sns.regplot(x="7 day", y="Sentiment", data=frame2,ci=None,color="#1dad9b")
    a7.set(xlabel= "Day 7 log return",ylabel="Sentiment")
    sns.plt.show()
    c1 = np.correlate(frame2['Sentiment'],frame2['1 day'])
    c2 = np.correlate(frame2['Sentiment'],frame2['3 day'])

    for x in range(7):
        string =str(x+1)+' day'
        x = frame2[string].values
        y = frame2['Sentiment'].values
        X = []
        Y = []
        for i in range(len(x)):
            if not np.isnan(x[i]) or np.isnan(y[i]):
                X.append(x[i])
                Y.append(y[i])
        slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
        print string
        print 'slope = {}, intercept= {}, r_value={}, p_value={}, std_err={}'.format(slope, intercept, r_value, p_value, std_err)
        C1 = frame2[string].corr(frame2['Sentiment'])
        print string +" correlation with sentiment : {}\n".format(C1)

def plotTradeVsNews(tickName):
    path2 = "resultsMKII"
    frame = getNewsNTradingVol(tick_Name,path2)
    newsBuz = []
    tradingVol = []
    newsVol = []
    for i in range(len(frame['tradingVol'])):
        newsBuz.append(frame['NewsBuz'].values[i])
        tradingVol.append(np.log(frame['tradingVol'].values[i]))
        newsVol.append(np.log(frame['NewsVol'].values[i]))
    sns.set(style="ticks")
    x = np.array(newsBuz)
    y = np.array(tradingVol)
    ax = sns.jointplot(x,y,kind="hex",stat_func=kendalltau,color="#4CB391")
    ax.set_axis_labels(xlabel= "News Buz",ylabel="Trading Volume")
    g = sns.jointplot(x, y, kind="kde", size=7, space=0)
    g.set_axis_labels(xlabel= "News Buz",ylabel="Trading Volume")

    x = np.array(newsVol)
    ay = sns.jointplot(x,y,kind="hex",stat_func=kendalltau,color="#4CB391")
    ay.set_axis_labels(xlabel= "News Volume",ylabel="Trading Volume")

    h = sns.jointplot(x, y, kind="kde", size=7, space=0)
    h.set_axis_labels(xlabel= "News Volume",ylabel="Trading Volume")
    sns.plt.show()
    # sns.plt.subplot(2,1,1)#41B3D3
    # a1 = sns.regplot(x="NewsBuz", y="tradingVol", data=frame,ci=None,fit_reg=False,color="#1dad9b")
    # a1.set_ylim([0,4e8])
    # sns.plt.subplot(2,1,2)
    #
    # a2 = sns.regplot(x="NewsVol", y="tradingVol", data=frame,ci=None,fit_reg=False,color="#41B3D3")
    # a2.set_ylim([0,4e8])
    sns.plt.show()

def sentimentAccuracy(tickeName):
    path2 = 'resultsMKII'
    frame2 = call_data(tick_Name,path2)
    logReturn = [[],[],[]]
    sentiment = []
    index = []
    for i in range(len(frame2)):
        for x in range(3):
            logReturn[x].append(frame2[str(x+1)+' day'].values[i])
        sentiment.append(frame2['Sentiment'].values[i])
        index.append(i)
    result = {'logReturn1':pd.Series(logReturn[0],index = index),
              'logReturn2':pd.Series(logReturn[1],index = index),
              'logReturn3':pd.Series(logReturn[2],index = index),
              'Sentiment':pd.Series(sentiment,index = index)}

    sns.plt.subplot(3,1,1)
    aw = sns.barplot(x="Sentiment",y = "logReturn1",ci=None,data = result)
    aw.set(xlabel='Sentiment', ylabel='Day 1')
    sns.plt.subplot(3,1,2)
    ax = sns.barplot(x="Sentiment",y = "logReturn2",ci=None,data = result)
    ax.set(xlabel='Sentiment', ylabel='Day 2')
    sns.plt.subplot(3,1,3)
    ay = sns.barplot(x="Sentiment",y = "logReturn3",ci=None,data = result)
    ay.set(xlabel='Sentiment', ylabel='Day 3')
    sns.plt.show()

def historyEffectOnSentiment(tickeName):
    # from mpl_toolkits.mplot3d import Axes3D
    path2 = 'resultsMKII'
    frame2 = call_data(tick_Name,path2)
    logReturn = [[],[],[],[],[]]
    sentiment = []
    index = []
    for i in range(len(frame2)):
        for x in range(5):
            logReturn[x].append(frame2['-'+str(x+1)+' day'].values[i])
        sentiment.append(frame2['Sentiment'].values[i])
        index.append(i)
    result = {'logReturn1':pd.Series(logReturn[0],index = index),
              'logReturn2':pd.Series(logReturn[1],index = index),
              'logReturn3':pd.Series(logReturn[2],index = index),
              'logReturn4':pd.Series(logReturn[3],index = index),
              'logReturn5':pd.Series(logReturn[4],index = index),
              'Sentiment':pd.Series(sentiment,index = index)}
    sns.plt.subplot(5,1,1)
    aw = sns.barplot(x="Sentiment",y = "logReturn1",data = result)
    aw.set(xlabel='Sentiment', ylabel='Day -1')
    sns.plt.subplot(5,1,2)
    ax = sns.barplot(x="Sentiment",y = "logReturn2",data = result)
    ax.set(xlabel='Sentiment', ylabel='Day -2')
    sns.plt.subplot(5,1,3)
    ay = sns.barplot(x="Sentiment",y = "logReturn3",data = result)
    ay.set(xlabel='Sentiment', ylabel='Day -3')
    sns.plt.subplot(5,1,4)
    az = sns.barplot(x="Sentiment",y = "logReturn4",data = result)
    az.set(xlabel='Sentiment', ylabel='Day -4')
    sns.plt.subplot(5,1,5)
    bx = sns.barplot(x="Sentiment",y = "logReturn5",data = result)
    bx.set(xlabel='Sentiment', ylabel='Day -5')
    sns.plt.show()


def surfacePlot(tickName):
    path2 = 'resultsMKII'
    frame2 = call_data(tick_Name,path2)
    logreturn = []
    logreturnNeg = []
    sentiment = []
    index = []
    points = np.random.rand(len(frame2),2)
    for i in range(len(frame2)):
        for x in range(1):
            points[i][0] = frame2['-'+str(x+1)+' day'].values[i]
            logreturnNeg.append(frame2['-'+str(x+1)+' day'].values[i])
            logreturn.append(frame2[str(x+1)+' day'].values[i])
        sentiment.append(frame2['Sentiment'].values[i])
        points[i][1] = frame2['Sentiment'].values[i]
        index.append(i)

    dict = {'day1 logReturn':pd.Series(logreturn,index = index),
                      'day-1 logReturn1':pd.Series(logreturnNeg,index = index),
                      'sentiment':pd.Series(sentiment,index = index)}
    df = pd.DataFrame(dict)
    df.to_csv('day1.csv')
    from scipy.interpolate import griddata
    values = np.asarray(logreturn)
    grid_x, grid_y = np.mgrid[-0.5:1:300j, -5:5:11j]
    grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')

    plt.imshow(grid_z0.T, extent=(-0.5,1,-5,5), origin='lower',aspect='auto',cmap="coolwarm")
    plt.xlabel('past log return')
    plt.ylabel('sentiment')
    plt.colorbar()
    plt.title('nearest , grid_x=300, grid_y = 11')
    plt.show()

    grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    plt.imshow(grid_z1.T, extent=(-0.5,1,-5,5), origin='lower',aspect='auto',cmap="coolwarm")
    plt.xlabel('past log return')
    plt.ylabel('sentiment')
    plt.title('Linear, grid_x=300, grid_y = 11')
    plt.colorbar()
    plt.show()

    # result = {'logreturnneg':pd.Series(logReturnNeg[0],index = index),
    #           'logreturnpos':pd.Series(logReturnPos[0],index = index),
    #           'sentiment':pd.Series(sentiment,index = index)}
    # df = pd.DataFrame(result)
    # data = df.pivot_table("logreturnpos", "sentiment", "logreturnneg", aggfunc=np.mean)
    # ax = sns.heatmap(data, cmap="YlGnBu")
    # ax.set(xlabel='Day -1 log return', ylabel='sentiment')
    # ax.set_xticklabels(data.columns.values, rotation =90)
    # sns.plt.show()
def surfacePlot2(tickName):
    import scipy
    path2 = 'resultsMKII'
    frame2 = call_data(tick_Name,path2)
    logreturn = []
    logreturnNeg = []
    sentiment = []
    index = []
    points = np.random.rand(len(frame2),2)
    for i in range(len(frame2)):
        for x in range(1):
            points[i][0] = frame2['-'+str(x+1)+' day'].values[i]
            logreturnNeg.append(frame2['-'+str(x+1)+' day'].values[i])
            logreturn.append(frame2[str(x+1)+' day'].values[i])
        sentiment.append(frame2['Sentiment'].values[i])
        points[i][1] = frame2['Sentiment'].values[i]
        index.append(i)
    X = np.asarray(logreturnNeg)
    Y = np.asarray(sentiment)
    Z = np.asanyarray(logreturn)
    d = scipy.stats.binned_statistic_2d(X,Y,Z,statistic="mean",bins =30)
    extent = [d[1][0], d[1][-1], d[2][0], d[2][-1]]
    plt.imshow(d[0].T, extent=(-0.5,1,-5,5), origin='lower',aspect='auto',cmap="coolwarm",interpolation='none')
    plt.colorbar()
    area = np.pi * (10 * np.random.rand(50))**2
    # plt.scatter(X,Y, s=area, c=Z, edgecolor='0.8',alpha=0.5)
    plt.xlabel('past log return')
    plt.ylabel('sentiment')
    plt.title('Day 1 Heatmap, Mean')
    plt.show()

if __name__ == '__main__':
    # name = 'INTEL_CORP'
    tick_Name = ['TESLA','FACEBOOK','APPLE_INC','EXXON_MOBIL','JPMORGAN','BANK_OF_AMERICA','GENERAL_MOTOR','AMAZON','MICROSOFT','INTEL_CORP','ABBOTT_LABORATORIES','ALLERGAN_INC','MONSANTO_CO','SYNGENTA_AG','YAHOO_INC','3M_CO','CATERPILLAR_INC','EBAY_INC','GENERAL_ELECTRIC_CO','MASTER_CARD']
    plotSentimenAndTime(tick_Name)
    plotTradeVsNews(tick_Name)
    historyEffectOnSentiment(tick_Name)
    surfacePlot2(tick_Name)



