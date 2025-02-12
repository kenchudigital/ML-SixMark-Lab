import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup

def update_data():

    df = pd.read_json('data/data.json')

    current_year = datetime.datetime.now().year

    response = requests.get(f'http://www.nfd.com.tw/house/year/{current_year}.htm')
    response.encoding = 'big5'
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    if table:
        data = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)     
    else:
        print('error')   
    new_df = pd.DataFrame(data[1:], columns=data[0])

    filtered_df = df[df['YEAR'] != current_year]
    df = pd.concat([filtered_df, new_df], ignore_index=True)
    df.to_json('data/data.json')

if __name__ == "__main__":
    update_data()

