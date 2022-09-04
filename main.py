    
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

#parse arguments, --api is the steamgriddb api key, -g is game folder, -n is number of options to download
parser = argparse.ArgumentParser()
parser.add_argument('--api', help='Steamgriddb api key')
parser.add_argument('-g', help='Game folder')
parser.add_argument('-n', help='Number of options to download')
args = parser.parse_args()
api_key = args.api
game_folder = args.g
number_to_download = args.n
if number_to_download is None:
    number_to_download = 1



#get current user
user = os.getlogin()

#save these arguments to a file so we can use them later
if(api_key is not None and game_folder is not None):
    with open('arguments.txt', 'w') as f:
        f.write(api_key + '\n')
        f.write(game_folder + '\n')
    print('Arguments saved, next time you can just run the script without arguments')

#if there are no arguments then load them from the file
if not api_key or not game_folder:
    with open('arguments.txt', 'r') as f:
        api_key = f.readline().rstrip()
        game_folder = f.readline().rstrip()
    print('Loaded arguments from file')

#make directory to save the images (in steam folder/custom_art)
save_dir = "/home/" + user + "/.local/share/Steam/custom_art/"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

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
            if i > (number_to_download-1):
                break
            print("downloading " + type + " image for " + game_name + " - " + str(i+1) + " of " + str(number_to_download))
            #download the image to grid folder while spoofing the user agent as a browser            
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(image['url'], save_dir + game_name + '_' + type + '.jpg')

#download the images
for game in games:
    download_images(game)