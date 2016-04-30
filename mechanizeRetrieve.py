__author__ = 'zytam'

import mechanize
import cookielib, sys
import random, os
import datetime, time, calendar
import json

class getUrl_Class:

    def __init__(self):

        self.br = mechanize.Browser() # Browser
        cj = cookielib.LWPCookieJar() # Cookie Jar
        self.br.set_cookiejar(cj)
        self.br.set_handle_equiv(True) # Browser options
        #br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1) # Follows refresh 0 but not hangs on refresh > 0
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] # User-Agent (this is cheating, ok?)

        self.token = 'pJrsdeoyrvwTL3H3uJ8h'

    def form_HKEX_url(self,ticker):
        ticker = ticker.zfill(5) # pad with zeroes
        # HKEX_url = 'https://www.quandl.com/api/v1/datasets/HKEX/' + ticker + '.json?auth_token=' + self.token
        HKEX_url = 'https://www.quandl.com/api/v1/datasets/HKEX/' + ticker + '.csv?auth_token=' + self.token
        return HKEX_url

    def form_HK_Yahoo_url(self,ticker):
        ticker = ticker.zfill(4)
        # yahoo_url = 'https://www.quandl.com/api/v1/datasets/YAHOO/HK_' + ticker +'.json?auth_token='+ self.token
        yahoo_url = 'https://www.quandl.com/api/v1/datasets/YAHOO/HK_' + ticker +'.csv?auth_token='+ self.token
        # https://www.quandl.com/api/v1/datasets/YAHOO/HK_2827.csv?auth_token=pJrsdeoyrvwTL3H3uJ8h
        return yahoo_url

    def get_url(self,url):
        self.br.open( url ) # The site we will navigate into, handling it's session
        html = self.br.response().read()
        return html

if __name__ == '__main__':

    ticker = '1057'

    get_url_obj = getUrl_Class()

    HKEX_url = get_url_obj.form_HKEX_url(ticker)
    yahoo_url = get_url_obj.form_HK_Yahoo_url(ticker)

    print HKEX_url
    print yahoo_url

    hkex_json = get_url_obj.get_url( HKEX_url )
    yahoo_json = get_url_obj.get_url( yahoo_url )

    import pandas as pd
    from StringIO import StringIO

    hkex_data = StringIO( hkex_json )
    hkex_df = pd.DataFrame.from_csv( hkex_data )
    hkex_data.seek(0) # go back to the start before it can be used for dataframe conversion again

    yahoo_data = StringIO( yahoo_json )
    yahoo_df = pd.DataFrame.from_csv( yahoo_data )


    # HKEX_json1 = json.load( hkex_json )
    # yahoo_json1 = json.load( yahoo_json )
