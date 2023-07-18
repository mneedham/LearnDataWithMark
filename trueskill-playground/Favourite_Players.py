import streamlit as st
import csv
import random
from player import Player
from trueskill import Rating

with open("data/players.csv", "r") as players_file:
    reader = csv.DictReader(players_file)
    players = [Player(row["name"], int(row["ranking"])) for row in reader]

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

if not "players" in st.session_state:
    st.session_state["players"] = players


st.write("# Favourite tennis players to watch 👋")

st.write("Select your favourite matches to watch and then learn who your favourite players are.")