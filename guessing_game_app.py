import streamlit as st
import random
from pathlib import Path
from sqlalchemy import text

# Page config
st.set_page_config(
    page_title="Guess the Number 🎯",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----- Custom Styling -----
custom_css = """
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {
        background-color: #121212;
        color: #f8f0fc;
        border-radius: 10px;
        padding: 2rem;
    }
    input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #1f1b24 !important;
        color: #f8f0fc !important;
    }
    button[kind="primary"] {
        background-color: #d6336c !important;
        color: white !important;
    }
    button[kind="secondary"] {
        background-color: #9c36b5 !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #f06595;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----- App Title -----
st.title("🎯 Number Guessing Game")

# ----- SQLite Leaderboard Connection -----
conn = st.connection("leaderboard_db", type="sql")

with conn.session as session:
    session.execute(text("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            name TEXT,
            attempts INTEGER
        )
    """))
    session.commit()

def get_leaderboard(limit=5):
    with conn.session as session:
        result = session.execute(text("SELECT name, attempts FROM leaderboard ORDER BY attempts ASC LIMIT :lim"), {"lim": limit})
        return result.fetchall()

def add_score(name, attempts):
    with conn.session as session:
        session.execute(text("INSERT INTO leaderboard (name, attempts) VALUES (:n, :a)"), {"n": name, "a": attempts})
        session.commit()

# ----- Session State Initialization -----
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# ----- Setup Section -----
if not st.session_state.game_started:
    player_name_input = st.text_input("👤 What's your name?", key="player_input_name")

    col1, col2 = st.columns(2)
    with col1:
        min_num = st.number_input("Min number", value=1, min_value=1, max_value=999)
    with col2:
        max_num = st.number_input("Max number", value=100, min_value=min_num + 1, max_value=1000)

    difficulty = st.selectbox("🎮 Choose difficulty:", ["Easy", "Medium", "Hard"])
    max_attempts = {"Easy": 10, "Medium": 6, "Hard": 3}[difficulty]

    if st.button("▶️ Start Game"):
        st.session_state.player_name = player_name_input.strip() or "Player"
        st.session_state.min_num = min_num
        st.session_state.max_num = max_num
        st.session_state.max_attempts = max_attempts
        st.session_state.comp_no = random.randint(min_num, max_num)
        st.session_state.attempts = 0
        st.session_state.hint_used = False
        st.session_state.game_over = False
        st.session_state.game_started = True
        st.experimental_rerun()

# ----- Game Play -----
if st.session_state.game_started:
    st.write(f"🎮 Hello **{st.session_state.player_name}**! Guess between **{st.session_state.min_num}** and **{st.session_state.max_num}**.")
    st.write(f"❤️ You have **{st.session_state.max_attempts}** attempts.")

    if not st.session_state.hint_used and not st.session_state.game_over:
        if st.button("🧠 Need a hint?"):
            lo = max(st.session_state.comp_no - 5, st.session_state.min_num)
            hi = min(st.session_state.comp_no + 5, st.session_state.max_num)
            st.info(f"🔍 It's between **{lo}** and **{hi}**.")
            st.session_state.hint_used = True

    if not st.session_state.game_over:
        guess = st.number_input("🎯 Your guess:", min_value=st.session_state.min_num, max_value=st.session_state.max_num, step=1)

        if st.button("🚀 Submit Guess"):
            st.session_state.attempts += 1
            guess_count = st.session_state.attempts
            comp = st.session_state.comp_no
            max_att = st.session_state.max_attempts

            if guess == comp:
                st.success(f"🎉 Correct! It was {comp}. You won in {guess_count} tries!")
                st.balloons()
                st.session_state.game_over = True
                add_score(st.session_state.player_name, guess_count)
            elif guess_count >= max_att:
                st.error(f"💥 Game Over! The number was {comp}.")
                st.session_state.game_over = True
            elif guess < comp:
                st.info("🔼 Try a **higher** number.")
            else:
                st.info("🔽 Try a **lower** number.")

            st.write(f"📊 Attempts: {guess_count} / {max_att}")

# ----- Game Over Section -----
if st.session_state.get("game_over", False):
    if st.button("🔄 Play Again"):
        st.session_state.game_started = False
        st.experimental_rerun()

    st.markdown("## 🏆 Leaderboard")
    top_scores = get_leaderboard()
    for i, row in enumerate(top_scores, start=1):
        # Try both attribute and dict access
        try:
            name = row.name
            attempts = row.attempts
        except AttributeError:
            name = row["name"]
            attempts = row["attempts"]

        st.markdown(f"{i}. **{name}** — {attempts} tries")
