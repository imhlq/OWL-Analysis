# Use to grad OWL-Match API

import requests
import pandas
import json
import os
import pickle

# Download matches Data
def download_data(folder='data', timeout=3):
    # Download match file
    if os.path.exists(folder+'/matches.json'):
        print('Use prepared match file')
    else:
        print('Download match file...')
        api_url = 'https://api.overwatchleague.com/matches'
        html = requests.get(api_url)
        data = html.json()
        with open(folder+'/matches.json', 'w') as fp:
            json.dump(data, fp)

    # ===================================================================

    if os.path.exists(folder+'/map_info.json'):
        print('Use prepared map info file')
    else:
        data = get_map_info()
        mapinfo = {}
        mapid = 0
        for evmap in data:
            mapinfo[evmap['guid']] = [mapid, evmap['name']['en_US'], evmap['name']['zh_CN']]
            mapid += 1
        with open(folder+'/map_info.json', 'w') as fp:
            json.dump(mapinfo, fp)

    # ===================================================================

    if os.path.exists(folder+'/maps.json'):
        print('Use prepared map files')
    else:
        fp = open(folder+'/matches.json')
        data = json.load(fp)['content']
        fp.close()
        print('Begin download Maps data...')
        stack_data = []
        num = 0
        for evmatch in data:
            # all matches
            if 'startDate' not in evmatch:
                continue

            matchid = evmatch['id']
            team1id = evmatch['competitors'][0]['id']
            team2id = evmatch['competitors'][1]['id'] 
            matchdate = evmatch['startDate']

            for evid, evmap in enumerate(evmatch['games']):
                # all maps
                if 'points' not in evmap:
                    print('Missed Map data.')
                    continue
                score = evmap['points']

                map_data = get_map_data(matchid, evid+1)    # map count from 1
                if map_data is None:
                    print('Fail Downloaded match:%d, map:%d' % (matchid, evid+1))
                    continue

                # Add extra information
                map_data['score'] = {'team1': team1id, 'team2':team2id, 'score': score}
                map_data['date'] = matchdate
                # add to stack
                stack_data.append(map_data)
                # output
                num += 1
                progress = num / (len(data) * 2.5) * 100
                print('[%.1f%%]Downloaded match:%d, map:%d' % (progress, matchid, evid+1))

        # save to file
        print('Writing to file...')
        fj = open(folder+'/maps.json', 'w')
        json.dump(stack_data, fj)
        fj.close()
        print('Finished!')



    return True

def get_map_info():
    api_url = 'https://api.overwatchleague.com/maps'
    html = requests.get(api_url)
    data = html.json()
    return data


def get_map_data(matchid, mapid):
    api_url = 'https://api.overwatchleague.com/stats/matches/{}/maps/{}'.format(matchid, mapid)
    html = requests.get(api_url)
    if html.status_code == 200:
        data = html.json()
        return data
    else:
        return None

def conv2int(mystr, idtype='mapid'):
    if idtype == 'hero_name':
        # heros
        heroesList = ['ana', 'ashe', 'bastion', 'baptiste', 'brigitte', 'doomfist', 'dva', 'genji', 'hanzo', 'junkrat', 'lucio', 'mccree', 'mei', 'mercy', 'moira', 'pharah', 'reaper', 'reinhardt', 'roadhog', 'soldier76', 'symmetra', 'torbjorn', 'tracer', 'widowmaker', 'winston' , 'wreckingball', 'zarya', 'zenyatta', 'sombra', 'orisa']
        return heroesList.index(mystr)

    elif idtype == 'mapid':
        # maps
        mapsList = ['0x080000000000066D', '0x08000000000002AF', '0x08000000000001DB', 
                    '0x0800000000000871', '0x08000000000000D4', '0x080000000000005B',
                    '0x08000000000005BB', '0x08000000000007E2', '0x08000000000006D3',
                    '0x080000000000069E', '0x08000000000004B7', '0x08000000000002C3',
                    '0x080000000000068D', '0x080000000000075E'
                    ]

    elif idtype=='maptype':
        # map_types
        typeList = ['ASSAULT', 'PAYLOAD', 'HYBRID', 'CONTROL']
        return typeList.index(mystr)

def wash_data(filepath='data/maps.json'):
    # batch:[match*map]
    # features: [mapid, teamid1, teamid2, heroes_s1, heroes_s2]
    # label: [match*map]*[team1win]
    # save as csv
    fp = open(filepath)
    data = json.load(fp)

    for evmap in data:
        # loop matches
        feature_names = ['mapid', 'team1id', 'team2id', ]
        label_name = ['score']


download_data()