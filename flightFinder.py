from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import datetime
import re
import csv

#Finds cheapest weekend flights for the 2019 calendar year
#using selenium and writes them to an csv file
#3 cheapest flight from each search



options = Options()
options.add_argument("--headless")

#set up location to webdriver
#I am using Firefox, but can be switched to Chrome if preferred  
driver = webdriver.Firefox(executable_path='YOUR_PATH_HERE', options=options)

#Change departure airport/city and file location.
startCity = 'JFK'
spreadsheet = csv.writer(open('flights'+startCity+'.csv', 'w'), delimiter=',')


spreadsheet.writerow(['Destination', 'Price', 'Nights','Depart Date', 'Return Date', 'Departure', 'URL'])
spreadsheet.writerow(['', '', '', '', '','' , ''])


for month in range(datetime.date.today().month,12):
    print('month: ' + str(month))
    #used for 2019 eom calendar year
    monthEnd = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    start = 1
    if(datetime.date.today().month == month):
        start = datetime.date.today().day
    for day in range(start,monthEnd[month]):
        print('day= '+str(day))
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
            time.sleep(3)
            #gets 3 cheapest flights (if found)
            for x in range(1,4):
                try:
                    priceB = '#trip-list-skipsy-tiles > li:nth-child('+str(x)+') > a > div.tile-header > div'
                    cityB = '#trip-list-skipsy-tiles > li:nth-child('+str(x)+') > a > div.tile-header > h2'
                    urlB = '#trip-list-skipsy-tiles > li:nth-child('+str(x)+') > a'
                    price = driver.find_element_by_css_selector(priceB).text.strip()
                    city = driver.find_element_by_css_selector(cityB).text.strip()
                    urlC = driver.find_element_by_css_selector(urlB).get_property('href')
                    city = ' '.join(city.split())
                    price = re.sub("[^\d\.]", "", price)
                    price = price[-3:].strip()
                    print(price[-3:] + ' ' + city + '\n'  )
                    spreadsheet.writerow([city, price, str(tempday-day),'2019-'+str(month).zfill(2)+'-'+str(day).zfill(2), '2019-'+str(tempMonth).zfill(2)+'-'+str(tempday).zfill(2), startCity, str(urlC)])
                except: 
                    print('no flights found for this date')
                    print(buildURL)
            print('---')
driver.close()