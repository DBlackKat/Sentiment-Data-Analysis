import pandas as pd
import pickle
import loadTicker
import quandl
import mechanize,os,re

def get_data(url):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_robots(False)
    br.set_handle_referer(True)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    response = br.open(url)
    if response.code == 404:
        return 0
    else:
        return br.response().read()

def gen_url(tickNumber,exchangeCode,API_KEYS):
    return "https://www.quandl.com/api/v3/datasets/NS1/"+str(tickNumber)+"_"+exchangeCode+".json?api_key="+str(API_KEYS)

def get_NS1(tickList,API_KEYS):
    outDir = os.path.join( os.getcwd(),'sentiment') # dir for all inputs and outputs
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    for idx,tic in enumerate(tick_List):
        pickle_path = os.path.join(os.getcwd(),'sentiment/'+tick_Name[idx]+'_NS1'+'.p')
        if os.path.isfile(pickle_path):
            print("{} exist, Skipping ...".format(tick_Name[idx]))
            continue
        print("Scrapping NS1/{}{} ...\n ".format(tic,'_US'))
        df =  quandl.get("NS1/"+tic+'_US',authtoken=API_KEYS)
        pickle.dump(df,open(pickle_path,'wb'))


def get_Exchange(tick):
    database = os.path.join( os.getcwd(),'GOOG-datasets-codes.csv') # dir for all inputs and outputs
    if not os.path.exists(database):
        br = mechanize.Browser()
        br.retrieve("https://www.quandl.com/api/v3/databases/GOOG/codes")
    df = pd.read_csv("GOOG-datasets-codes.csv",sep=',')
    df.columns = ['code','company']
    value = []
    for string in df['code']:
        if re.sub(r'.*_','',string) == tick:
            string = string.replace(tick,'')
            string = string.replace('GOOG/','')
            print string
            if string == 'NASDAQ_' or string == 'NYSE_':
                return string

    return 'error'

def getNASDAQ(tick_List,tick_Name,API_KEYS):
    outDir = os.path.join( os.getcwd(),'database') # dir for all inputs and outputs
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    for idx,tic in enumerate(tick_List):
        pickle_path = os.path.join(os.getcwd(),'database/'+tick_Name[idx]+'.p')
        if os.path.isfile(pickle_path):
            print("{} exist, Skipping ...".format(tick_Name[idx]))
            continue
        exchange = get_Exchange(tic)
        print("Scrapping GOOG/{}{} ...\n ".format(exchange,tic))
        df =  quandl.get("GOOG/"+exchange+tic,authtoken=API_KEYS)
        pickle.dump(df,open(pickle_path,'wb'))

if __name__ == '__main__':
    secret_Keys = "4FAJeN3Mof45xWy7kJTB"
    secret_Keys2 = "7nWBk8r-jkZAYHjS_suN"
    secret_Keys3 = "GgKrsJ1FuGKPqcTP3H3W"
    secret_Keys4 = "MjPxBBsc_beQd813tG4E"
    secret_Keys5 = "8DhiPjmLxR7xASuW4rsP"
    secret_Keys6 = "_zzziPSFhrUUYEM6WZNF"
    tick_List = ['TSLA','FB','AAPL','XOM','JPM','BAC','GM','AMZN','MSFT','INTC'] #selected ticker list
    tick_Name = ['TESLA','FACEBOOK','APPLE_INC','EXXON_MOBIL','JPMORGAN','BANK_OF_AMERICA','GENERAL_MOTOR','AMAZON','MICROSOFT','INTEL_CORP']

    targetExchange = 'US'

    getNASDAQ(tick_List,tick_Name,secret_Keys)
    get_NS1(tick_List,secret_Keys)
