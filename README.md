# SteamGridDBLoader
A simple tool to download and install SteamGridDB images for your games.

## Usage
1. Clone the repository or download and extract the zip.
2. run `pip install -r requirements.txt` to install the required packages.
3. run `python main.py --api <steamgriddb api key> -g <path to your directory of games>`
4. Add the custom art to your games in Steam from the custom_art folder in your steam directory. (/.steam/steam/custom_art on linux)

## Flags
* `--api` - The SteamGridDB API key. You can get one [here](https://www.steamgriddb.com/profile/settings/api).
* `-g` - The path to your directory of non-steam games.
* `-n` - Optional flag to set the number of images to download for each game. Defaults to 1.

## Notes
* After your first run, the program will save your API key and game path to config.txt, meaning you can run the program without the flags.
* Running this script will overwrite any art in custom_art previously downloaded by this script.

## Plans
* Fetch the games from your non-steam game shortcuts (shortcuts.vdf) instead of requiring a path to the games. (This is a bit more complicated than I thought it would be due to how shortcuts.vdf is structured.)
* Have the script automatically add the art to your games in Steam. (Again, relies on parsing the shortcuts.vdf)
* Add a GUI to let you select which art you want to download for each game. (Similar to Steam ROM Manager)

## Credits
* [SteamGridDB](https://www.steamgriddb.com/) for providing the images.
* Me, Jacob Ewen, for writing the script.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
