    
import os
import requests
import json
import shutil
import sys
import time
import urllib.request
import urllib.parse
import vdf
import argparse

#parse arguments, --api is the steamgriddb api key, -g is game folder
parser = argparse.ArgumentParser()
parser.add_argument('--api', help='Steamgriddb api key')
parser.add_argument('-g', help='Game folder')
args = parser.parse_args()
api_key = args.api
game_folder = args.g

games = []
#set games to the names of the folders in the game folder
for folder in os.listdir(game_folder):
    games.append(folder)


#search for game on steamgriddb
def get_gameid(game_name):
    print('Searching for game on steamgriddb...', game_name)
    #https://www.steamgriddb.com/api/v2/search/autocomplete/{term}
    url = 'https://www.steamgriddb.com/api/v2/search/autocomplete/' + game_name
    headers = {'Authorization': 'Bearer ' + api_key}
    response = requests.get(url, headers=headers)
    print(response)
    data = json.loads(response.text)
    if data['data']:
        return data['data'][0]['id']
    else:
        return None

#download the game images
def download_images(game_name):
    game_id = get_gameid(game_name)
    if game_id is None:
        print('Game not found on steam')
        return
    types = ["grids", "heroes", "logos", "icons"]
    #use steamgriddb api to get the images from game id then download them
    for type in types:
        url = 'https://www.steamgriddb.com/api/v2/'+type+'/game/' + str(game_id)
        headers = {'Authorization': 'Bearer ' + api_key}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        #download the first 1 images
        for i, image in enumerate(data['data']):
            if i > 0:
                break
            print(image['url'])
            #download the image to grid folder while spoofing the user agent as a browser            
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(image['url'], 'pics/' + game_name + '_' + type + '.jpg')

#download the images
for game in games:
    download_images(game)