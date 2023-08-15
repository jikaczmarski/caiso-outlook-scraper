# Download CAISO Supply Data

This tool was designed for researchers who need time series supply data from CAISO. The method used here is to webscrap the CAISO supply page, download daily supply data at the five minute interval, and then combine that data into a spreadsheet for use in econometric and statistical projects. As of now, there are two possible download sources: the supply trend and the renewables trend. The supply trend collapses all the renewable sources into one source which is often not sufficient for researchers.

This code was based off the kajpeterson repository, but is completely rewritten. The goal of such a rewrite was to fix the use of deprecated practices, improve speed and efficiency, and fix errors in the final dataset driven by certain handling of dates and times. Additionally, this scraper has both supply trends and renewable trends built into one scraper.

# Current Functional Status
_Currently working to update_
* Supply trend data: **Non-functioning** (08/15/2023)
* Renewables trend data: **Non-functioning** (08/15/2023)

# Requirements

This tool has two requirements:

1. Google Chrome
   - You need to know what version you are running as it matters for what driver you get.
2. Chrome Driver
   - Needs to be specific for your version of Chrome and you operating system. It *must* be placed in the `driver` folder. The one in this repository is for Chrome 102 with an M1 Macbook.

I encourage users of Firefox and other browsers to fork this repository and alter the selenium code for their browsers of choice.

# Setup

1. Obtain a copy of this repository
2. (Optional) Create a virtual environment based on requirements.txt and then enter that virtual environment
   - If you don't do this, then it will be a hassle to ensure you have the required packages, and using the requirements.txt file ensures that this program will run properly. YMMV with newer or older packages.

# Example

For this example, I will be downloading the supply trend data for January 10th, 2021 to January 13th, 2021. To do this, I first run program with the `-h` option to see what the required inputs are:
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
> (caisoenv) python caiso-scraper.py supply-trend supplyresults.csv 2019-01-10 2019-01-13
Sample covers 4 days.
downloading supply trend for 01/10/2019
downloading supply trend for 01/11/2019
downloading supply trend for 01/12/2019
downloading supply trend for 01/13/2019
Expected 1152 observations. Recieved 1152 observations.
```
The data will be saved to the `results` folder with the title I specified: `supplyresults.csv`. An example of the output file is provided below, but the file continues for the entire duration of the sample:
|datetime    |renewables|natural_gas|large_hydro|imports|batteries|nuclear|coal|other|
|------------|----------|-----------|-----------|-------|---------|-------|----|-----|
|1/10/19 0:00|3246      |7416       |1040       |7725   |4        |2264   |13  |0    |
|1/10/19 0:05|3281      |7507       |921        |7655   |1        |2264   |13  |0    |
|1/10/19 0:10|3311      |7598       |874        |7497   |22       |2263   |13  |0    |
|1/10/19 0:15|3352      |7533       |872        |7441   |36       |2263   |13  |0    |
|1/10/19 0:20|3380      |7453       |885        |7371   |33       |2263   |13  |0    |
|1/10/19 0:25|3440      |7390       |862        |7379   |-10      |2263   |13  |0    |
|1/10/19 0:30|3508      |7381       |832        |7363   |-53      |2263   |13  |0    |

### Disclaimer
It is rare, but there are several days where the data provided by CAISO is inaccurate or missing. Some examples off the top of my head are 02/18/2020 having five extra minutes in the day, and 01/02/2019 having no values for natural gas. It is important to know that this is not an error of this program, but an error that CAISO made. In my limited testing, going to the CAISO website and grabbing the data manually shows these errors. My workaround for the extra five minutes in a day is to just delete it (already built into the program) since most of the variables are equivalent to the first five minutes of the next day (but not all, specifically 02/18/2020 has a slightly different value for natural gas, but all else is equal).
