import requests
import os
from time import sleep

base = 'https://lambda-treasure-hunt.herokuapp.com/api/'

end = {
    'init': 'adv/init',
    'wear': 'adv/wear',
    'undress': 'adv/undress',
    'player': 'adv/player_state',
    'carry': 'adv/carry',
    'receive': 'adv/receive',
    'warp': 'adv/warp',
    'recall': 'adv/recall',
    'take': 'adv/take',
    'drop': 'adv/drop',
    'move': 'adv/move',
    'sell': 'adv/sell',
    'change': 'adv/transmogrify',
    'status': 'adv/status',
    'examine': 'adv/examine',
    'name': 'adv/change_name',
    'pray': 'adv/pray',
    'fly': 'adv/fly',
    'dash': 'adv/dash',
    'mine': 'bc/mine',
    'totals': 'bc/totals',
    'lp': 'bc/last_proof',
    'bal': 'bc/get_balance'
}

# token = os.environ.get('TOKEN')
headers = {'Authorization': "Token " +
           '486e036c24cba2433eea71c35d5f5a86f7315b63'}
sleep_time = 1


def post(endpoint, data):
    '''
    accepts (endpoint, data)
    Makes a post request to the given endpoint with
    Authorization header included from env file and 
    returns a jsonified response with cooldown
    '''
    req = requests.post(f'{base}{endpoint}/', json=data, headers=headers)
    json = req.json()
    if json['cooldown'] != 0:
        sleep_time = float(json['cooldown'])
    print(f'{endpoint} ----> {sleep_time} second cooldown')
    if len(json['errors']):
        for err in json['errors']:
            print('\nERROR --->', err, end='\n\n')
    sleep(sleep_time)
    return json


def get(endpoint):
    '''
    Makes a get request to the given endpoint with
    Authorization header included from env file and 
    returns a jsonified response
    '''
    req = requests.get(f'{base}{endpoint}/', headers=headers)
    json = req.json()
    if json['cooldown'] != 0:
        sleep_time = float(json['cooldown'])
    print(f'{endpoint} ----> {sleep_time} second cooldown')
    if len(json['errors']):
        for err in json['errors']:
            print('\nERROR --->', err, end='\n\n')
    sleep(sleep_time)
    return json
