import json
import requests



def main():
    response = requests.request('GET', 'https://badge.sha2017.org/eggs/list/json')

    # print(response)
    data = response.json()
    # print(data)
    hitlist = sorted(data, key=lambda x: x['download_counter'], reverse=True)
    
    for h in hitlist:
        print('{:10d} {:}'.format(h['download_counter'], h['name']))
    
    

if __name__ == '__main__':
    main()