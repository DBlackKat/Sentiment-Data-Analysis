import Quandl, arrow, glob, os, pickle
import quandlLib as ql
import mechanizeRetrieve as mr # import my custom functions
import pandas as pd
import numpy as np
import oracle_paths as op

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

def dl_GOOG_ticks(sub_db_name):

    get_url_obj = mr.getUrl_Class()
    req_url = 'https://s3.amazonaws.com/quandl-static-content/Ticker+CSV%27s/Google/{}.csv'.format(sub_db_name)
    tick_str = get_url_obj.get_url( req_url )

    # Fix delimiter
    head = tick_str[1:26]
    body = tick_str[26:]
    body = body.replace('.,','.')
    body = body.replace(', ',' ')
    body = body.replace(' ,',' ')

    # f = open('temp.txt','w')
    # f.write(head+body)
    # f.close()

    tick_csv = StringIO(head+body)
    df = pd.DataFrame.from_csv(tick_csv, sep=",")

    local_t = arrow.now().timestamp
    csv_lists = glob.glob( os.path.join(op.flat_files(),'GOOG_{}_alltick_*.csv'.format(sub_db_name)) )
    if len(csv_lists) > 0:
        os.remove( csv_lists[0] ) # Remove the old copy

    df.to_csv( os.path.join(op.flat_files(),'GOOG_{}_alltick_{}_.csv'.format(sub_db_name,local_t)),index=False)

    return df

def dl_db_ticks(db_name):

    print('Update Database Ticker Lists from Quandl: {}'.format(db_name))
    quandl_token = ql.read_token()
    get_url_obj = mr.getUrl_Class()

    cat_df = []
    for idx in np.arange(1,101):

        sys.stdout.write('\rDownloading Page: {} (Max Call: 100)'.format(idx))
        if idx == 100:
            print('===== Max Calls Reached! (in db creation) =====')

        req_url = 'https://www.quandl.com/api/v3/datasets.csv?database_code={}&per_page=100&sort_by=id&page={}&api_key={}'.format(db_name,idx,quandl_token)
        tick_str = get_url_obj.get_url( req_url )
        if len(tick_str) == 0:
            break

        tick_csv = StringIO(tick_str)
        df = pd.DataFrame.from_csv(tick_csv, sep=",", parse_dates=False)
        if len(cat_df) == 0:
            cat_df = df
        else:
            cat_df = cat_df.append(df)

    sys.stdout.write('\n')

    local_t = arrow.now().timestamp
    csv_lists = glob.glob( os.path.join(op.flat_files(),'{}_alltick_*.csv'.format(db_name)) )
    if len(csv_lists) > 0:
        os.remove( csv_lists[0] ) # Remove the old copy
    cat_df.to_csv( os.path.join(op.flat_files(),'{}_alltick_{}_.csv'.format(db_name,local_t)),index=False)

    return cat_df

def quandl_db_info(db_name):

    load_local = False
    csv_lists = glob.glob( os.path.join(op.flat_files(),'{}_alltick_*.csv'.format(db_name)) )

    if len(csv_lists) > 0:
        c_file_stamp = int( os.path.basename(csv_lists[0]).split('_')[-2] )
        if (arrow.now().timestamp - c_file_stamp) < 432000: # more than 5 days then update again
            load_local = True

    if load_local:
        print('Load Local Copy of Database Lists')
        cat_df = pd.read_csv(csv_lists[0])
    else:
        if 'GOOG_' in db_name: # Means we are dealing with a sub_db case
            cat_df = dl_GOOG_ticks(db_name.split('_')[1])
        else:
            cat_df = dl_db_ticks(db_name)

    return cat_df

def create_quandl_lib(db_name):

    db_info_df = quandl_db_info(db_name)

    quandl_token = ql.read_token()
    for db_row in db_info_df.iterrows():
        if 'GOOG_' in db_name:
            db_sym = db_row[1][0].split('/')[0]
            tick = db_row[1][0].split('/')[1]
            tick_name = db_row[1][1]
        else:
            db_sym = db_row[1][1]
            tick = '{0:0>5}'.format(db_row[1][0])
            tick_name = db_row[1][2]

        tick_path = os.path.join(op.pickle_files(),'{}_{}_.p'.format(db_sym,tick))
        if os.path.isfile(tick_path): # important to prevent overwriting potentially more complete local db
            print('{}/{} Exists in Local, Skipping ...'.format(db_sym,tick))
            continue

        print('Creating: {}/{}...'.format(db_sym,tick))
        try:
            tick_df = Quandl.get("{}/{}".format(db_sym,tick), authtoken=quandl_token)
        except:
            print('Error in Getting {}/{}'.format(db_sym,tick))
            continue

        tick_df.name = tick_name

        pickle.dump( tick_df, open( tick_path , "wb" ) )
        tick_df.to_csv( os.path.join(op.flat_files(),'{}_{}_.csv'.format(db_sym,tick))  )

    return 0

def update_db_new_ticks(db_name):

    cat_df = dl_db_ticks(db_name)
    db_ticks = ['{0:0>5}'.format(c) for c in cat_df.dataset_code.values]

    flat_lists = glob.glob( os.path.join(op.flat_files(),'{}*.csv'.format(db_name)) )
    flat_ticks = [os.path.basename(c).split('_')[1] for c in flat_lists]

    pickle_lists = glob.glob( os.path.join(op.pickle_files(),'{}*.p'.format(db_name)) )
    pickle_ticks = [os.path.basename(c).split('_')[1] for c in pickle_lists]

    db_not_in_flat = np.sum( ~np.in1d(db_ticks,flat_ticks) )
    db_not_in_pickle = np.sum( ~np.in1d(db_ticks,pickle_ticks) )

    print('Flat Missing: {}, Pickle Missing: {}'.format(db_not_in_flat,db_not_in_pickle))
    if db_not_in_flat > 0 or db_not_in_pickle > 0: # then need to find the missing ones and add to db

        if db_not_in_flat + db_not_in_flat == db_not_in_flat:
            print('===== Unbalanced Match!!!! =====')

        quandl_token = ql.read_token()
        # Iter over the not in local db lists, flat file first
        not_in_local_bool = ~np.in1d(db_ticks,flat_ticks)
        for c_tick in db_ticks[not_in_local_bool]:
            tick_df = Quandl.get("{}/{}".format(db_name,c_tick), authtoken=quandl_token)
            tick_df.to_csv( os.path.join(op.flat_files(),'{}_{}_.csv'.format(db_name,c_tick))  )

        # Inefficient, but do not care, cause not expected to happen often
        not_in_local_bool = ~np.in1d(db_ticks,pickle_ticks)
        for c_tick in db_ticks[not_in_local_bool]:
            tick_df = Quandl.get("{}/{}".format(db_name,c_tick), authtoken=quandl_token)
            tick_df.name = cat_df.name.values[np.in1d(db_ticks,c_tick)][0]
            pickle.dump( tick_df, open( os.path.join(op.pickle_files(),'{}_{}_.p'.format(db_name,c_tick)) , "wb" ) )

        print('DB Update Complete!')
    else:
        print('Tick and Local and Cloud Matched!')

    return 1

def update_db(db_name=[]):

    # Blind update we update whatever
    # smart update we based on the trading day of HKEX

    # List all the files with db name
    if len(db_name) == 0:
        db_lists = glob.glob( os.path.join(op.pickle_files(),'*.p'.format(db_name)) )
    else:
        db_lists = glob.glob( os.path.join(op.pickle_files(),'{}_*.p'.format(db_name)) )

    for c_file in db_lists:
        file_name = os.path.basename(c_file)
        db_name = file_name.split('_')[0]
        tick_name = file_name.split('_')[1]
        update_selected_quandl('{}/{}'.format(db_name,tick_name))

    return 1

def update_selected_quandl(tick):

    db_name = tick.split('/')[0]
    tick_name = tick.split('/')[1]

    tick_path = os.path.join(op.pickle_files(),'{}_{}_.p'.format(db_name,tick_name))
    quandl_token = ql.read_token()
    if os.path.isfile(tick_path):

        sys.stdout.write('Updating: {} ... '.format(tick))

        tick_df = pickle.load( open( tick_path, "rb" ) ) # load the file and check the most recent entry
        c_df = Quandl.get(tick, trim_start=tick_df.index.values[-1].astype("S64")[0:10],authtoken=quandl_token)
        new_tick_df = pd.merge(tick_df,c_df,how='outer')

        if new_tick_df.shape == tick_df.shape:
            sys.stdout.write('No new entries ... ')
        else:
            sys.stdout.write('Save to pickle ... ')
            pickle.dump( new_tick_df, open( tick_path , "wb" ) )

        sys.stdout.write('Done!\n')

    else:
        print('{} Not Found in local DB'.format(tick))

    return 1


def get_quandl_tick(tick_lists):

    tick_dict = {}
    # Search through local files, if cannot find download through quandl api
    quandl_token = ql.read_token()
    for c_tick in tick_lists:
        db_name = c_tick.split('/')[0]
        tick_name = c_tick.split('/')[1]

        tick_path = os.path.join(op.pickle_files(),'{}_{}_.p'.format(db_name,tick_name))
        if os.path.isfile(tick_path):
            tick_df = pickle.load( open( tick_path, "rb" ) ) # load the file and check the most recent entry
        else:
            try:
                tick_df = Quandl.get(c_tick,authtoken=quandl_token)
                pickle.dump( tick_df, open( tick_path , "wb" ) )
            except:
                tick_df = []
                print('Error in Getting {}'.format(c_tick))

        if len(tick_df) > 0:
            tick_dict[c_tick] = tick_df

    return tick_dict


def db_pickle2csv(db_name=[]):

    return 1


if __name__ == '__main__':

    db_name = 'HKEX'
    # create_quandl_lib(db_name)
    # update_db_new_ticks(db_name)
    # update_db(db_name)
    # get_quandl_tick(['GOOG/HKG_0126'])

    # dl_GOOG_ticks('HKG')
    create_quandl_lib('GOOG_HKG')

    # a = pickle.load( open( "HKEX_00001_.p", "rb" ) ) # Take 2.59 ms
    # a = pd.read_csv("HKEX_00001_.csv") # 3.02ms
