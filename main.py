    
import os
import requests
import json
import shutil
import sys
import time
import urllib.request
import urllib.parse

# prompt user for game folder
game_folder = input("Enter the path to the game folder: ")

#prompt user for steamgriddb api key
api_key = input("Enter your steamgriddb api key: ")

# Get the game name from the folder name
game_name = os.path.basename(game_folder)

#find steam folder userdata
steam_folder = os.path.expanduser('~') + '/.steam/steam/userdata'

#prompt user to select steam account
print('Select Steam Account:')
for i, folder in enumerate(os.listdir(steam_folder)):
    print(i, folder)
account = int(input('Account: '))
steam_folder = steam_folder + '/' + os.listdir(steam_folder)[account]

#enter config grid folder
grid_folder = steam_folder + '/config/grid'

#check if grid folder exists
if not os.path.exists(grid_folder):
    os.makedirs(grid_folder)

#down the game images from steamgriddb
def download_image(url, filename):
    with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

#search for game on steamgriddb
def search_game(game_name):
    url = 'https://www.steamgriddb.com/api/v2/search/autocomplete/' + urllib.parse.quote(game_name)
    headers = {'Authorization': 'Bearer ' + api_key}
    response = requests.get(url, headers=headers)
    return response.json()

#download the game images
def download_images(game_name):
    game = search_game(game_name)
    if game:
        for i, game in enumerate(game):
            print(i, game['name'])
        choice = int(input('Select game: '))
        game = game[choice]
        print('Downloading images for ' + game['name'])
        for i, image in enumerate(game['images']):
            print(i, image['filename'])
        choice = int(input('Select image: '))
        image = game['images'][choice]
        download_image(image['url'], grid_folder + '/' + game['name'] + '.jpg')
        download_image(image['url'], grid_folder + '/' + game['name'] + '.png')
    else:
        print('No game found')
