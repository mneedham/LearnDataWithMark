import streamlit as st
import csv
import random
from player import Player

st.header("Top ranking players")

if not "players" in st.session_state:
    st.write("No players found")
else:
    players = st.session_state["players"]
    sorted_players = sorted(players, key = lambda player: player.rating, reverse=True)
    
    player_dicts = [{
        "name": player.name, 
        "rank": player.rank, 
        "rating": player.rating.mu,
        "certainty": player.rating.sigma,
        "comparisons": player.comparisons
        } 
        for player in sorted_players[0:20]]

    st.table(player_dicts)
