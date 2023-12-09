# Unsupported

This project has been superseded by [caiso-data-downloader](https://github.com/JesseKaczmarski/caiso-data-downloader). This project is no longer being maintained but will remain for educational purposes.

# Download CAISO Supply Data

This tool was designed for researchers who need time series supply data from CAISO. The method used here is to webscrap the CAISO supply page, download daily supply data at the five minute interval, and then combine that data into a spreadsheet for use in econometric and statistical projects. As of now, there are two possible download sources: the supply trend and the renewables trend. The supply trend collapses all the renewable sources into one source which is often not sufficient for researchers.

# Current Functional Status

* Supply trend data: **Fully functional** (09/14/2023)
* Renewables trend data: **Fully functional** (09/14/2023)

# Requirements

This tool has two requirements:

1. Google Chrome
2. Chrome Driver
   - Needs to be specific for your version of Chrome and you operating system. It *must* be placed in the `./driver` folder. This repository provides the chromedriver: `.../116.0.5845.96/mac-arm64/chromedriver-mac-arm64`. Chromedrivers for older versions of Chrome can be found [here](https://chromedriver.chromium.org/downloads) and newer versions can be found at [here](https://googlechromelabs.github.io/chrome-for-testing/#stable)


# Setup

1. Obtain a copy of this repository
2. Create a virtual environment and install the packages in `./requirements.txt`

# Example

For this example, I will be downloading the supply trend data for January 1, 2023 to January 5, 2023. To do this, I first run program with the `-h` option to see what the required inputs are:
```
> (caisoenv) python caiso-scraper.py -h
usage: caiso-scraper.py [-h] source filename startdate enddate

A web scraper tool to download CAISO supply data.

positional arguments:
  source      Either supply-trend or renewables-trend
  filename    The name of the output file with .csv extension (e.g. filename.csv)
  startdate   String input: YYYY-MM-DD
  enddate     String input: YYYY-MM-DD

optional arguments:
  -h, --help  show this help message and exit
```
Given my above example, the code I will need will be:
```
> (caisoenv) python caiso-scraper.py supply-trend supplyresults.csv 2023-01-01 2023-01-05
Successfully created csv download location.
Successfully created results location.
Data source: supply-trend 
 Results location: /Users/jikaczmarski/Documents/programming/python/caiso-data-downloader-main/results/supplyresults.csv 
 Sample begins: Jan 01, 2023 
 Sample ends: Jan 05, 2023 
 Sample length: 5 days ( 1440 observations )
Loading web driver...
Results saved to ../results/supplyresults.csv
No missing observations found.
```
The data will be saved to the `results` folder with the title I specified: `supplyresults.csv`. An example of the output file is provided below, but the file continues for the entire duration of the sample:
|datetime|renewables                   |natural_gas|large_hydro                                  |imports|batteries|nuclear|coal|other|
|--------|-----------------------------|-----------|---------------------------------------------|-------|---------|-------|----|-----|
|1/1/23 0:00|4751                         |8225       |1477                                         |6129   |200      |2245   |4   |0    |
|1/1/23 0:05|4991                         |8098       |1496                                         |5889   |259      |2244   |3   |0    |
|1/1/23 0:10|5175                         |7888       |1405                                         |5898   |231      |2246   |3   |0    |
|1/1/23 0:15|5384                         |7637       |1416                                         |5785   |321      |2245   |3   |0    |

### Disclaimer
It is rare, but there are several days where the data provided by CAISO is inaccurate or missing. It is important to know that this is not an error of this program, but an error that CAISO made.
