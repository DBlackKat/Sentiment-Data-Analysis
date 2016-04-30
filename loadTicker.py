import numpy as np
import pandas as pd
import os
import mechanize
class getTicker:
    def __init__(self):
        database = os.path.join( os.getcwd(),'NS1-datasets-codes.csv') # dir for all inputs and outputs
        if not os.path.exists(database):
            br = mechanize.Browser()
            br.retrieve("https://www.quandl.com/api/v3/databases/NS1/codes")
    def returnTicker(self,exchangeCode):
        df= pd.read_csv("NS1-datasets-codes.csv",sep=',')
        df.columns = ['code','company']
        value = []
        for string in df['code']:
            if string[-2:] == exchangeCode:
                string = string.replace('NS1/','')
                string = string.replace('_'+exchangeCode,'')
                value.append(string)
        return value

def returnticker(exchangeCode):
    df= pd.read_csv("NS1-datasets-codes.csv",sep=',')
    df.columns = ['code','company']
    value = []
    for string in df['code']:
        if string[-2:] == exchangeCode:
            string = string.replace('NS1/','')
            string = string.replace('_'+exchangeCode,'')
            value.append(string)
    return value

if __name__ == '__main__':
    get = getTicker()
    value = get.returnTicker("HK")
    print value