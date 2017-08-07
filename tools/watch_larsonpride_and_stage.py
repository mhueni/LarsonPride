import json
import requests



def main():
    response = requests.request('GET', 'https://badge.sha2017.org/eggs/list/json')

    # print(response)
    data = response.json()
    # print(data)
    hitlist = sorted(data, key=lambda x: x['download_counter'], reverse=True)

    print('{:5} {:10} {:30} {}'.format('score', 'downloads', 'name', 'revision'))

    for index, h in enumerate(hitlist):
        if h['name'] in ['Larson Pride', 'LarsonStage']:
            h['score'] = index
            print('{:5} {:10} {:30} {}'.format(h['score'], h['download_counter'], h['name'], h['revision']))
        
    # with open('last_data.json', 'w') as last_json_file:
    #     json.dump(data, last_json_file)
    

if __name__ == '__main__':
    main()