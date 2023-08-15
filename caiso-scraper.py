from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import argparse
from datetime import datetime, timedelta, date
import os
import glob
import pandas as pd
import csv
import time
import sys
import numpy as np

parser = argparse.ArgumentParser(description="A web scraper tool to download CAISO supply data.")

def valid_file_inputs(d):
    if d.endswith(".csv") == True:
        return d
    else:
        filename_error_message = "Not a valid filename input. Missing .csv extension."
        raise argparse.ArgumentTypeError(filename_error_message)

def valid_date_inputs(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        date_error_message = "Not a valid date input: {0!r}".format(s)
        raise argparse.ArgumentTypeError(date_error_message)

def valid_sources(y):
    source_list = ['supply-trend','renewables-trend',]
    if y in source_list:
        return y
    else:
        print('Not an acceptable source. See the readme for options.')
        exit()

parser.add_argument('source', type=valid_sources, help='Either supply-trend or renewables-trend')
parser.add_argument('filename', type=valid_file_inputs, help='The name of the output file with .csv extension (e.g. filename.csv)')
parser.add_argument('startdate', type=valid_date_inputs, help='String input: YYYY-MM-DD')
parser.add_argument('enddate', type=valid_date_inputs, help='String input: YYYY-MM-DD')
args = parser.parse_args()

if args.startdate > args.enddate:
    print('Error: Provided start date exceeds the end date.')
    exit()
else:
    pass

if args.startdate < datetime.strptime('2018-04-10','%Y-%m-%d'):
    print('Error: Start date exceeds available data. Earliest available data is Apr 10, 2018.')
    exit()
else:
    pass

if args.enddate > (datetime.now() - timedelta(days=1)):
    print('Error: No data available for dates into the future. You entered:',args.enddate.strftime("%b %d%, %Y"))
    exit()
else:
    pass

input_delta = args.enddate - args.startdate

path = sys.path[0]
csvdir = f'{path}/csvraw/'
resultsdir = f'{path}/results/'

try:
    os.mkdir(csvdir)
    print("Successfully created csv download location.")
except FileExistsError:
    pass

try:
    os.mkdir(resultsdir)
    print("Successfully created results location.")
except FileExistsError:
    pass

print(
    "Data source:", args.source, os.linesep,
    "Results location:", resultsdir + args.filename, os.linesep,
    "Sample begins:", args.startdate.strftime("%b %d%, %Y"), os.linesep,
    "Sample ends:", args.enddate.strftime("%b %d%, %Y"), os.linesep,
    "Sample length:", (input_delta.days + 1), "days (", (input_delta.days + 1)*288, "observations )"
)
print('Loading web driver...')
chromedriver = './driver/chromedriver'
os.chmod(chromedriver, 0o0755)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
prefs = {"download.default_directory" : csvdir}
options.add_experimental_option("prefs",prefs)
ser = Service(chromedriver)
browser = webdriver.Chrome(service=ser, options=options)


browser.get('http://www.caiso.com/TodaysOutlook/Pages/supply.aspx')

elements = browser.find_elements(By.TAG_NAME, 'input')
downloaded_files = []
if args.source == "supply-trend":
    for element in elements:
        if 'supply-trend-date' in element.get_attribute('class'):
            while args.startdate <= args.enddate:
                download_counter = input_delta.days + 1
                element.click()
                element.clear()
                date_input = args.startdate.strftime('%m/%d/%Y')
                element.send_keys(date_input)
                element.send_keys(Keys.ENTER)

                button1 = browser.find_element(By.XPATH, '//*[@id="dropdownMenuSupplyDownload"]')
                time.sleep(2)
                button1.click()
                button2 = browser.find_element(By.XPATH, '//*[@id="downloadSupplyCSV"]')

                while True:
                    try:
                        button2.click()
                        print("downloading", date_input, end='\r')
                    except:
                        time.sleep(0.5)
                        print("needed a nap")
                        continue
                    break

                downloaded_file_name = "CAISO-supply-" + args.startdate.strftime('%Y%m%d') + ".csv"
                downloaded_files.append(downloaded_file_name)
                args.startdate = args.startdate + timedelta(days=1)

    browser.close()
elif args.source == "renewables-trend":
    for element in elements:
        if 'renewables-date' in element.get_attribute('class'):
            while args.startdate <= args.enddate:
                download_counter = input_delta.days + 1
                element.click()
                element.clear()
                date_input = args.startdate.strftime('%m/%d/%Y')
                element.send_keys(date_input)
                element.send_keys(Keys.ENTER)

                button1 = browser.find_element(By.XPATH, '//*[@id="dropdownMenuRenewables"]')
                time.sleep(2)
                button1.click()
                button2 = browser.find_element(By.XPATH, '//*[@id="downloadRenewablesCSV"]')

                while True:
                    try:
                        button2.click()
                        download_counter = download_counter - 1
                        print("downloading", date_input, end='\r')
                    except:
                        time.sleep(0.5)
                        print("needed a nap")
                        continue
                    break
                downloaded_file_name = "CAISO-renewables-" + args.startdate.strftime('%Y%m%d') + ".csv"
                downloaded_files.append(downloaded_file_name)
                args.startdate = args.startdate + timedelta(days=1)

    browser.close()
else:
    quit()

if args.source == "supply-trend":
    df = pd.DataFrame(columns=['datetime','renewables','natural_gas','large_hydro','imports','batteries','nuclear','coal','other'])
    missingObservations = []
    for filename in os.listdir(csvdir) and downloaded_files:
        dftmp = pd.read_csv(csvdir + filename, header=None)
        date = (dftmp[0][0]).lstrip('Supply ').rstrip('undefined')
        dftmp = dftmp.T
        dftmp = dftmp.iloc[1:]
        dftmp = dftmp[dftmp[0] != "24:00"] # Error fix for some downloads having a 24th hour timestamp.
        #dftmp['datetime'] = pd.to_datetime(date + " " + dftmp.iloc[:,0], format="%m/%d/%Y %H:%M") # ValueError: time data "01/10/2019undefined 0:00" doesn't match format "%m/%d/%Y %H:%M", at position 0.
        dftmp['datetime'] = pd.to_datetime(date + " " + dftmp.iloc[:,0], format="%m/%d/%Y %H:%M")
        dftmp.rename(columns={0:'time',1:'renewables',2:'natural_gas',3:'large_hydro',4:'imports',5:'batteries',6:'nuclear',7:'coal',8:'other'},inplace=True)
        del dftmp['time']
        dftmp = dftmp[['datetime','renewables','natural_gas','large_hydro','imports','batteries','nuclear','coal','other']]
        df = pd.concat([df, dftmp],ignore_index=True)

    df = df.dropna(how="all")
    df.to_csv(resultsdir + str(args.filename),index=False)
    print("Results saved to",resultsdir + str(args.filename),end='\n')
    missingObservations = pd.date_range(df['datetime'].min(), df['datetime'].max(), freq='5min').difference(df['datetime'])
    if len(missingObservations) != 0:
        with open(resultsdir + args.filename.rstrip('.csv') +'-missingObservations.txt', 'w') as fp:
            fp.write("Missing observations: \n")
            for item in missingObservations:
                fp.write("%s\n" % item)
            print('Missing observations found. For a list, see:',resultsdir + args.filename.rstrip('.csv') +'-missingObservations.txt',end='\n')
    else:
        print('No missing observations found.')

elif args.source == "renewables-trend":
    df = pd.DataFrame(columns=['datetime','solar','wind','geothermal','biomass','biogas','small_hydro'])
    missingObservations = []
    for filename in os.listdir(csvdir) and downloaded_files:
        dftmp = pd.read_csv(csvdir + filename, header=None)
        date = (dftmp[0][0]).lstrip('Renewables ')
        dftmp = dftmp.T
        dftmp = dftmp.iloc[1:]
        dftmp['datetime'] = pd.to_datetime(date + " " + dftmp.iloc[:,0], format="%m/%d/%Y %H:%M")
        dftmp.rename(columns={0:'time',1:'solar',2:'wind',3:'geothermal',4:'biomass',5:'biogas',6:'small_hydro'},inplace=True)
        del dftmp['time']
        dftmp = dftmp[['datetime','solar','wind','geothermal','biomass','biogas','small_hydro']]
        df = pd.concat([df, dftmp],ignore_index=True)

    df = df.dropna(how="all")
    df.to_csv(resultsdir + str(args.filename),index=False)
    print("Results saved to",resultsdir + str(args.filename),end='\n')
    missingObservations = pd.date_range(df['datetime'].min(), df['datetime'].max(), freq='5min').difference(df['datetime'])
    if len(missingObservations) != 0:
        with open(resultsdir + args.filename.rstrip('.csv') +'-missingObservations.txt', 'w') as fp:
            fp.write("Missing observations: \n")
            for item in missingObservations:
                fp.write("%s\n" % item)
            print('Missing observations found. For a list, see:',resultsdir + args.filename.rstrip('.csv') +'-missingObservations.txt',end='\n')
    else:
        print('No missing observations found.')
else:
    pass

quit()
