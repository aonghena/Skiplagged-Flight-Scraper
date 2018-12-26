from selenium import webdriver
from webbrowser import Chrome
from selenium.webdriver.common.keys import Keys
import time
import datetime
import re
import csv

#Finds cheapest weekend flights for the 2019 calendar year
#using selenium and writes them to an csv file
#3 cheapest flight from each search

#set up location to webdriver
driver = webdriver.Chrome(executable_path='YOURPATHHERE')

#Change departure airport/city and file location if needed
startCity = 'JFK'
spreadsheet = csv.writer(open('flights.csv', 'w'), delimiter=',')

spreadsheet.writerow(['Destination', 'Price', 'Depart Date', 'Return Date', 'Departure'])
spreadsheet.writerow(['', '', '', '', ''])

for month in range(1,12):
    print(month)
    #used for 2019 eom calendar year
    monthEnd = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for day in range(1,monthEnd[month]):
        #week day calc
        weekDay = datetime.date(2019, month, day).isoweekday()
        expDay = weekDay - 5
        if(expDay == 0):
            expDay = 3
        elif(expDay == 1):
            expDay = 2
        elif(expDay == 2):
            expDay = 1
        #Used to find multi-day flights on weekends.
        for t in range(0,expDay):
            tempMonth = month
            tempday = t+day
            if(tempday > monthEnd[month]):
                tempday = 1
                tempMonth += 1
            buildURL = 'https://skiplagged.com/flights/'+str(startCity)+'/2019-'+str(month).zfill(2)+'-'+str(day).zfill(2)+'/2019-'+str(tempMonth).zfill(2)+'-'+str(tempday).zfill(2)
            driver.get(buildURL)
            time.sleep(7)
            #gets 3 cheapest flights (if found)
            for x in range(1,4):
                try:
                    priceB = '#trip-list-skipsy-tiles > li:nth-child('+str(x)+') > a > div.tile-header > div'
                    cityB = '#trip-list-skipsy-tiles > li:nth-child('+str(x)+') > a > div.tile-header > h2'
                    price = driver.find_element_by_css_selector(priceB).text.strip()
                    city = driver.find_element_by_css_selector(cityB).text.strip()
                    price = re.sub("[^\d\.]", "", price)
                    price = price[-3:].strip()
                    print(price[-3:] + ' ' + city + '\n'  )
                    spreadsheet.writerow([city, price, '2019-'+str(month).zfill(2)+'-'+str(day).zfill(2), '2019-'+str(tempMonth).zfill(2)+'-'+str(tempday).zfill(2), startCity])
                except: 
                    print('no flights found for this date')
            time.sleep(2)
            print('---')