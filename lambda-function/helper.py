
"""Helper functions to assist in checking for errors and for specific cases"""

import bs4 as bs
import urllib.request
import urllib.parse
from collections import defaultdict
import difflib


def try_ex(func):
    """Call passed in function in try block. If KeyError is encountered return
    None. This function is intended to be used to safely access dictionary.
    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def is_valid_lot(parking_lot):
    """Check if passed parking lot is valid. Uses difflib to check the ratio.
    if the raito of the checked word vs the actual word is equal to or above
    the limit, then the checked word is converted to the actual word.

    Returns a dictionary containing whether the checked lot is valid and the
    corrected spelling of the word."""

    if parking_lot is None:
        # If no parking lot is given, return
        return {'isValid': True, 'newLotName': None}

    parking_lot = parking_lot.lower()

    valid_lots = [
        'EvFree Church', 'State College Structure', 'Lot A & G',
        'Eastside Structure', 'Nutwood Structure', 'Brea Mall', 'all',
        'everywhere'
    ]

    max_ratio = 0
    is_valid = False
    lot = None
    limit = 0.7

    for valid_lot in valid_lots:
        # Go through each lot and compare the ratios. If the ratio is high
        # enough then save that lot
        ratio = difflib.SequenceMatcher(None, valid_lot.lower(),
                                        parking_lot).ratio()
        if valid_lot == 'Nutwood Structure':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'nutwood',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'State College Structure':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'state college',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'Eastside Structure':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'eastside',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'EvFree Church':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'evfree',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'church',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'Brea Mall':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'brea',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'mall',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'Lot A & G':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'lot g & a',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'lot a', parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'a', parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'g', parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'a and g',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'g and a',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif ratio >= limit and ratio >= max_ratio:
            is_valid = True
            lot = valid_lot
            max_ratio = ratio

    return {'isValid': is_valid, 'newLotName': lot}


def build_validation_result(is_valid, violated_slot, message_content):
    """Creates the results for whether a parking lot is valid or not"""

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {
            'contentType': 'PlainText',
            'content': message_content
        }
    }


def validate_parking_lot(slots):
    """Checks whether the user's requested lot is valid"""

    parking_lot = try_ex(lambda: slots['ParkingLot'])
    validation = is_valid_lot(parking_lot)

    if parking_lot and not validation['isValid']:
        return build_validation_result(
            False,
            'ParkingLot',
            'I do not know of any information regarding {}, try a different '
            'parking location.'.format(parking_lot)
        )

    return {
        'isValid': True,
        'newLotName': validation['newLotName']}


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


def get_lot_names():
    return [
        'Nutwood Structure', 'State College Structure',
        'Eastside Structure', 'Lot A & G',
        'EvFree Church', 'Brea Mall'
        ]


def get_available_lots():
    """Returns a dict containgin two lists; one that contains closed parking
    lots, another that contains open parking lots
    """

    parking_data = scrape_data()
    lot_names = get_lot_names()
    closed_lots = []
    avail_lots = []

    for name in lot_names:
        strip_name = name.replace(' ', '')
        if parking_data[strip_name]['AvailableSpaces'] in ('Closed', 'FULL'):
            closed_lots.append(name)
        else:
            avail_lots.append(name)

    return {'ClosedLots': closed_lots, 'AvailableLots': avail_lots}


def get_optimal_lots():
    """Returns a dictionary that has the parking data sorted.

    Example:
    sorted_parking['First']['Name']
    returns the name of the parking lot with the most parking spaces

    sorted_lots['Second']['AvailableSpaces']
    returns the available spaces for the parking with the second most parking
    spaces.
    """

    parking_lots = scrape_data()
    sorted_lots = defaultdict(dict)

    positions = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth']
    lot_names = get_lot_names()

    # Sort the lots.
    for position in positions:
        max_num = 0
        for name in lot_names:
            strip_name = name.replace(' ', '')

            if parking_lots[strip_name]['AvailableSpaces'] in ('Closed', 'FULL'):
                parking_lots[strip_name]['AvailableSpaces'] = 0

            if int(parking_lots[strip_name]['AvailableSpaces']) >= max_num:
                max_num = int(parking_lots[strip_name]['AvailableSpaces'])
                optimal_lot = name

        lot_names.remove(optimal_lot)
        sorted_lots[position]['Name'] = optimal_lot
        sorted_lots[position]['AvailableSpaces'] = str(max_num)

    return sorted_lots


def build_optimal_msg(sorted_lots):
    """Creates fulfillment message for the list intent"""

    if sorted_lots['First']['AvailableSpaces'] == '0':
        return 'All parking locations are either full or closed right now. ' \
               'This includes: Nutwood Structure, State College Structure, ' \
               'Eastside Structure, Lot A & G, EvFree Church, Brea Mall.'

    return '{} is the best place to park right now. It has {} available ' \
           'parking spaces.'.format(
               sorted_lots['First']['Name'],
               sorted_lots['First']['AvailableSpaces']
           )


def build_list_lot_msg():
    """"Creates the fulfillment message for the list intent."""

    lot_list = get_available_lots()

    if not lot_list['ClosedLots']:
        # If there are no closed lots, create the message with only open lots.
        available_lots = lot_list['AvailableLots'][0]
        del lot_list['AvailableLots'][0]
        for lot in lot_list['AvailableLots']:
            available_lots += (', ' + lot)

        return 'All parking locations are open right now! This includes: ' \
               '{}.'.format(available_lots)

    elif not lot_list['AvailableLots']:
        # If there are no open lots, create the message with only open lots.
        closed_lots = lot_list['ClosedLots'][0]
        del lot_list['ClosedLots'][0]
        for lot in lot_list['ClosedLots']:
            closed_lots += (', ' + lot)

        return 'All parking locations are either full or closed right now. ' \
               'This includes {}'.format(closed_lots)

    else:
        available_lots = lot_list['AvailableLots'][0]
        del lot_list['AvailableLots'][0]
        for lot in lot_list['AvailableLots']:
            available_lots += (', ' + lot)

        closed_lots = lot_list['ClosedLots'][0]
        del lot_list['ClosedLots'][0]
        for lot in lot_list['ClosedLots']:
            closed_lots += (', ' + lot)

        return 'Today you can park at: {}. You cannot park at: ' \
               '{}.'.format(available_lots, closed_lots)


def build_specific_parking_msg(parking_lot):
    """"Creates the fulfillment message for the specific parking intent."""

    parking_data = scrape_data()
    lot_name = parking_lot.replace(' ', '')

    if lot_name == 'all' or lot_name == 'everywhere':
        return 'Here are the available spaces for all locations: ' \
               'Nutwood Structure ({}), State College Structure({}), ' \
               'Eastside Structure ({}), Lot A & G ({}), ' \
               'EvFree Church ({}), Brea Mall ({})'.format(
                    parking_data['NutwoodStructure']['AvailableSpaces'],
                    parking_data['StateCollegeStructure']['AvailableSpaces'],
                    parking_data['EastsideStructure']['AvailableSpaces'],
                    parking_data['LotA&G']['AvailableSpaces'],
                    parking_data['EvFreeChurch']['AvailableSpaces'],
                    parking_data['BreaMall']['AvailableSpaces']
                )
    elif parking_data[lot_name]['AvailableSpaces'] == 'Closed':
        return '{} is currently close. It is open on {}.'.format(
                    parking_lot,
                    parking_data[lot_name]['Date']
                )
    elif parking_data[lot_name]['AvailableSpaces'] == 'FULL':
        return '{} is currently full.'.format(parking_lot)
    else:
        return "{} currently has {} available parking spaces.".format(
                    parking_lot,
                    parking_data[lot_name]['AvailableSpaces']
                )


def build_directions_msg(parking_lot):
    """"Creates the fulfillment message for the directions intent."""

    parking_data = scrape_data()
    lot_name = parking_lot.replace(' ', '')

    if lot_name == 'all' or lot_name == 'everywhere':
        return 'Here are the directions for all locations: ' \
               'Nutwood Structure ({}), State College Structure({}), ' \
               'Eastside Structure ({}), Lot A & G ({}), ' \
               'EvFree Church ({}), Brea Mall ({})'.format(
                    parking_data['NutwoodStructure']['Directions'],
                    parking_data['StateCollegeStructure']['Directions'],
                    parking_data['EastsideStructure']['Directions'],
                    parking_data['LotA&G']['Directions'],
                    parking_data['EvFreeChurch']['Directions'],
                    parking_data['BreaMall']['Directions']
                )
    else:
        return 'Here are the directions to {}: {}'.format(
                    parking_lot,
                    parking_data[lot_name]['Directions']
        )
