    
import os
import requests
import json
import shutil
import sys
import time
import urllib.request
import urllib.parse

#check if there are command line arguments

if len(sys.argv) > 1:
    print("args ok")
    #first arg is game_folder
    game_folder = sys.argv[1]
    #second arg is api_key
    api_key = sys.argv[2]
    #third arg is steam_folder
    steam_folder = sys.argv[3]
else:
    print("args not ok")
    #end program if no command line arguments
    sys.exit()

games = []
#loop through the game folders and get the folder names
for folder in os.listdir(game_folder):
    games.append(folder)

#replace spaces with underscores in games
for i, game in enumerate(games):
    games[i] = game.replace(' ', '_')

#find steam folder userdata

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
    print(game_id)
    #use steamgriddb api to get the images from game id then download them
    url = 'https://www.steamgriddb.com/api/v2/grids/game/' + str(game_id)
    headers = {'Authorization': 'Bearer ' + api_key}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    #download the first 5 images
    for i, image in enumerate(data['data']):
        if i > 4:
            break
        print(image['url'])
        #download the image to grid folder while spoofing the user agent as a browser            
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(image['url'], 'temp/' + game_name + '_' + str(i) + '.jpg')

#download the images
for game in games:
    download_images(game)

#display the images in temp and prompt user to select image
def select_image(game_name):
    print('Select image for', game_name)
    for i, image in enumerate(os.listdir('temp')):
        if game_name in image:
            print(i, image)
    image = int(input('Image: '))
    return image

#move the selected image to the grid folder
def move_image(game_name, image):
    print('Moving image to grid folder...')
    shutil.move('temp/' + os.listdir('temp')[image], grid_folder + '/' + game_name + '.jpg')

#loop through the games and select the image
for game in games:
    image = select_image(game)
    move_image(game, image)

#delete images in temp folder
for image in os.listdir('temp'):
    os.remove('temp/' + image)