from trueskill import quality_1vs1, rate_1vs1, rate
import csv

from player import Player

with open("data/players.csv", "r") as players_file:
    reader = csv.DictReader(players_file)
    players = [Player(row["name"], int(row["ranking"])) for row in reader]


top_10 = (player for player in players if player.rank <= 10)

p1 = next(top_10)
p2 = next(top_10)
p3 = next(top_10)
p4 = next(top_10)

t1 = [p1.rating, p4.rating]
t2 = [p2.rating, p3.rating] 

(p1_new, p4_new), (p2_new, p3_new) = rate([t1, t2], ranks=[0, 1])

p1.rating = p1_new
p2.rating = p2_new
p3.rating = p3_new
p4.rating = p4_new