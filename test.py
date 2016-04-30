import pandas as pd
import os
from math import floor
def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

if __name__ == '__main__':
    name = 'TESLA'
    pickle_path = os.path.join(os.getcwd(),'results/'+name+'_NS1.p')
    df = pd.read_pickle(pickle_path)
    margin1 = []
    margin2 = []
    margin3 = []
    sentiment = []
    idx = []
    for x in range(len(df['Buy'])):
        margin1.append(floored_percentage((df['1stDay'][x]-df['Buy'][x])/df['Buy'][x],3))
        margin2.append(floored_percentage((df['3rdDay'][x]-df['Buy'][x])/df['Buy'][x],3))
        margin3.append(floored_percentage((df['5thDay'][x]-df['Buy'][x])/df['Buy'][x],3))
        sentiment.append(df['sentiment'][x])
        idx.append(x+1)
    d = {'1 day margin':pd.Series(margin1,index = idx),
         '3 day margin':pd.Series(margin2,index = idx),
         '5 day margin':pd.Series(margin3,index = idx),
         '  Sentiment':pd.Series(sentiment,index = idx)}
    df = pd.DataFrame(d)
    print df
