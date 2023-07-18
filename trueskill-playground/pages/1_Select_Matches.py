import streamlit as st
import random
from player import Player
from trueskill import quality_1vs1, rate_1vs1, rate
import numpy as np

st.markdown("""
    <style>
        .stButton>button {
            color: black;
            background-color: white;
            border-radius: 0.5em;
            border: 2px solid #00008B;
            padding: 20px;
            margin: 1em 0 0 0em ;
            width: 100%;
            height: 100%;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00008B;
            color:white;
            font-weight:700;
            border: 2px solid #00008B;
        }

        .stButton>button:active {
            background-color: #00008B;
            color:white;
            font-weight:700;
        }

        .stButton>button:focus {
            outline: none;
        }
    </style>
""", unsafe_allow_html=True)

def compute_weight(rank):
    if rank <= 20:
        return np.exp(-rank/5)  # Strong bias
    elif rank <= 50:
        return np.exp(-rank/10)  # Medium bias
    elif rank <= 100:
        return np.exp(-rank/20)  # Weak bias
    else:
        return np.exp(-rank/50)  # Very weak bias

def update_rankings(winning_pair, losing_pair, no_preference=False):
    t1 = [p.rating for p in winning_pair]
    t2 = [p.rating for p in losing_pair]

    if no_preference:
        (p1_new, p2_new), (p3_new, p4_new) = rate([t1, t2], ranks=[0, 0])
    else: 
        (p1_new, p2_new), (p3_new, p4_new) = rate([t1, t2], ranks=[0, 1])

    p1, p2 = winning_pair
    p3, p4 = losing_pair

    p1.update_rating(p1_new)
    p2.update_rating(p2_new)
    p3.update_rating(p3_new)
    p4.update_rating(p4_new)

if not "players" in st.session_state:
    st.write("No players to choose from")
else:
    players = st.session_state["players"]

    st.header("Which tennis match would you watch?")

    weights = [compute_weight(player.rank) for player in players]
    weights = weights / np.sum(weights)

    selected_players = list(np.random.choice(players, size=4, replace=False, p=weights))

    pair1 = selected_players[:2]
    pair2 = selected_players[2:]

    col1, col2, col3 = st.columns(3)
    with col1:
        button1 = st.button(f"{pair1[0].name}  \n vs  \n  {pair1[1].name}", key="pair1", on_click=lambda: update_rankings(pair1, pair2))

    with col2:
        button1 = st.button("I don't  \n have a  \n  preference", key="neither", on_click=lambda: update_rankings(pair1, pair2, no_preference=True) )

    with col3:
        button2 = st.button(f"{pair2[0].name}  \n vs  \n  {pair2[1].name}", key="pair2", on_click=lambda: update_rankings(pair2, pair1))