import streamlit as st
import random

# Page config
st.set_page_config(
    page_title="Guess the Number 🎯",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark theme and custom styling
custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

st.title("🎯 Number Guessing Game")

# STEP 1: Collect setup inputs (enabled until user starts game)
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

if not st.session_state.game_started:
    # Name input
    name = st.text_input("👤 What's your name?", key="name")
    
    col1, col2 = st.columns(2)
    with col1:
        min_num = st.number_input("Min number", value=1, min_value=1, max_value=999)
    with col2:
        max_num = st.number_input("Max number", value=100, min_value=min_num + 1, max_value=1000)
    
    # Difficulty selection
    difficulty = st.selectbox("🎮 Choose difficulty:", ["Easy", "Medium", "Hard"])
    
    # Compute attempts
    if difficulty == "Easy":
        max_attempts = 10
    elif difficulty == "Medium":
        max_attempts = 6
    else:
        max_attempts = 3

    # Start button
    if st.button("▶️ Start Game"):
        # Store everything in session state
        st.session_state.game_started = True
        st.session_state.name = name if name else "Player"
        st.session_state.min_num = min_num
        st.session_state.max_num = max_num
        st.session_state.difficulty = difficulty
        st.session_state.max_attempts = max_attempts
        st.session_state.comp_no = random.randint(min_num, max_num)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.hint_used = False
        st.experimental_rerun()

# STEP 2: Game UI (starts only after clicking Start Game)
if st.session_state.game_started:

    st.write(f"🎮 Hello **{st.session_state.name}**! Guess a number between **{st.session_state.min_num}** and **{st.session_state.max_num}**.")
    st.write(f"❤️ You have **{st.session_state.max_attempts}** attempts.")

    # Hint
    if not st.session_state.hint_used and not st.session_state.game_over:
        if st.button("🧠 Need a hint?"):
            hint_range = 5
            hint_lower = max(st.session_state.comp_no - hint_range, st.session_state.min_num)
            hint_upper = min(st.session_state.comp_no + hint_range, st.session_state.max_num)
            st.info(f"🔍 It's between **{hint_lower}** and **{hint_upper}**.")
            st.session_state.hint_used = True

    # Gameplay
    if not st.session_state.game_over:
        guess = st.number_input("🎯 Your guess:", min_value=st.session_state.min_num, max_value=st.session_state.max_num, step=1)
        if st.button("🚀 Submit Guess"):
            st.session_state.attempts += 1
            comp = st.session_state.comp_no
            att = st.session_state.attempts
            max_att = st.session_state.max_attempts

            if guess == comp:
                st.success(f"🎉 Correct! It was **{comp}**. You won in {att} attempts.")
                st.balloons()
                st.session_state.game_over = True
                st.session_state.leaderboard.append((st.session_state.name, att))
                st.session_state.leaderboard.sort(key=lambda x: x[1])
            elif att >= max_att:
                st.error(f"💥 Game Over! The number was **{comp}**.")
                st.session_state.game_over = True
            elif guess < comp:
                st.info("🔼 Try a **higher** number.")
            else:
                st.info("🔽 Try a **lower** number.")

            st.write(f"📊 Attempts used: {att} / {max_att}")

    # Restart
    if st.session_state.game_over:
        if st.button("🔄 Restart Game"):
            st.session_state.game_started = False
            st.session_state.comp_no = None
            st.session_state.attempts = 0
            st.session_state.hint_used = False
            st.session_state.game_over = False
            st.experimental_rerun()

    # Leaderboard
    if st.session_state.leaderboard:
        st.markdown("## 🏆 Leaderboard")
        for i, (player, score) in enumerate(st.session_state.leaderboard[:5], start=1):
            st.markdown(f"{i}. **{player}** — {score} tries")
