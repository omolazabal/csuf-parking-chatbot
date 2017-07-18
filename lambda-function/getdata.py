import bs4 as bs
import urllib.request
import urllib.parse


url = 'https://parking.fullerton.edu/parkinglotcounts/mobile.aspx'
source = urllib.request.urlopen(url)
soup_obj = bs.BeautifulSoup(source, 'lxml')

table = soup_obj.table
table_rows = table.find_all('tr')

lot_data = {}

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text.strip() for i in td]
    lot_info = row[0].split('\n')
    lot_info[0] = lot_info[0].replace(':', '').replace(' ', '')
    lot_info[1] = lot_info[1].replace(':', '').replace(' ', '')
    lot_info.append(row[1].split('\n')[0])

#    lot_data[lot_info[0][]] = 
