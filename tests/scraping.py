import bs4 as bs
import urllib.request
import urllib.parse
from collections import defaultdict


def scrape_data():
    """A dictionary will be returned. It contains information about the various
    parking locations at csuf.

    Parking locations currently used in parking_lots:
        Nutwood Structure
        State College Structure
        Eastside Structure
        Lot A & G
        EvFree Church
        Brea Mall

    Available information for the parking locaitons:
        Total Spaces
        Date (last date the information was updated)
        Time (last time the information was updated)
        Available Spaces
        Directions

    To access information about a specific parking lot enter the full name of
    the parking location (the ones listed above) with camel case as the first
    dimension, then enter the information you want to access (the ones listed
    above) with camel case. For example:

        parking_lots['LotA&G']['TotalSpaces']
            returns total amount of spaces available

    """
    url = 'https://parking.fullerton.edu/parkinglotcounts/mobile.aspx'
    source = urllib.request.urlopen(url)
    soup_obj = bs.BeautifulSoup(source, 'html.parser')

    table = soup_obj.table
    table_rows = table.find_all('tr')

    data_type = ['TotalSpaces', 'Date', 'Time',
                 'AvailableSpaces', 'Directions']

    parking_lots = defaultdict(dict)
    directions = [
        'https://goo.gl/af6i12', 'https://goo.gl/KzsZqZ',
        'https://goo.gl/U14f9D', 'https://goo.gl/tc82nc',
        'https://goo.gl/qTh7fL', 'https://goo.gl/RKnN5k'
    ]

    for tr, direction in zip(table_rows, directions):
        td = tr.find_all('td')

        # Returns a list containing the data on the left column (row[0]) and
        # the data on the right column (row[1]).
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
        for type_, index in zip(data_type, range(2, 7)):
            if index == 6:
                parking_lots[lot_data[0]][type_] = direction
            else:
                parking_lots[lot_data[0]][type_] = lot_data[index]

    return parking_lots


print(scrape_data())
