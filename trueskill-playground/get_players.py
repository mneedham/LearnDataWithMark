import requests
from bs4 import BeautifulSoup
import csv

def get_player_names(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # specify the encoding
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        player_columns = soup.select('div#plyrRankings table tbody tr td.pn')

        return [column.contents[0] for column in player_columns]

url = "https://live-tennis.eu/en/atp-live-ranking"

with open("players.csv", 'w', encoding='utf-8') as players_file:
    writer = csv.writer(players_file, delimiter=",")
    writer.writerow(["ranking", "name"])
    players = get_player_names(url)
    for index, player in enumerate(players):
        writer.writerow([index+1, player])
