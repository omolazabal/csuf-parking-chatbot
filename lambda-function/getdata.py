"""This file scrapes the parking data off the CSUF parking site"""

import bs4 as bs
import urllib.request
import urllib.parse


url = 'https://parking.fullerton.edu/parkinglotcounts/mobile.aspx'
source = urllib.request.urlopen(url)
soup_obj = bs.BeautifulSoup(source, 'lxml')

table = soup_obj.table
table_rows = table.find_all('tr')

parking_lots = {}

for tr in table_rows:
    td = tr.find_all('td')

    # Returns a list containing the data on the left column (row[0]) and the
    # data on the right column (row[1]).
    row = [i.text.strip() for i in td]

    # Split all of the contents of the row into a list.
    lot_data = row[0].split('\n')
    lot_data[0] = lot_data[0].replace(':', '').replace(' ', '')
    lot_data[1] = lot_data[1].replace(':', '').replace(' ', '')

    # Split the date and time cell into two seperate cells. Have to be wary
    # about whether the cell has a time or not.
    if lot_data[3].endswith('M'):
        # If string ends with AM or PM
        date_time = lot_data[3].split(' ', 1)
    else:
        date_time = [lot_data[3], None]
    del lot_data[3]
    lot_data.extend(date_time)

    # Append the available parking spaces column.
    lot_data.append(row[1].split('\n')[0])

    # Organize the data into the parking_lots dictionary.
    parking_lots[lot_data[0]] = {}
    parking_lots[lot_data[0]][lot_data[1]] = lot_data[2]  # TotalSpaces
    parking_lots[lot_data[0]]['Date'] = lot_data[3]
    parking_lots[lot_data[0]]['Time'] = lot_data[4]
    parking_lots[lot_data[0]]['AvailableSpaces'] = lot_data[5]
