import helper


def list_lots_msg():
    lot_list = helper.get_available_lots()

    if not lot_list['ClosedLots']:
        available_lots = lot_list['AvailableLots'][0]
        del lot_list['AvailableLots'][0]
        for lot in lot_list['AvailableLots']:
            available_lots += (', ' + lot)

        return 'All parking locations are open today! You can park' \
               ' at {}.'.format(available_lots)
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


def specific_parking_msg(parking_lot):
    parking_data = helper.scrape_data()
    lot_name = parking_lot.replace(' ', '')

    if lot_name == 'all':
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
    else:
        return "{} currently has {} available parking spaces.".format(
                    parking_lot,
                    parking_data[lot_name]['AvailableSpaces']
                )


def directions_msg(parking_lot):
    parking_data = helper.scrape_data()
    lot_name = parking_lot.replace(' ', '')

    if lot_name == 'all':
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
