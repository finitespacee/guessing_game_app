import streamlit as st
import random

# Page config
st.set_page_config(
    page_title="Guess the Number 🎯",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom dark theme + accents
custom_css = """
    <style>
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Background and text */
    .block-container {
        background-color: #121212;
        color: #f8f0fc;
        border-radius: 10px;
        padding: 2rem;
    }

    /* Widgets */
    div[data-baseweb="select"] > div {
        background-color: #1f1b24 !important;
        color: #f8f0fc !important;
    }
    input, .stNumberInput input {
        background-color: #1f1b24 !important;
        color: #f8f0fc !important;
    }

    /* Buttons */
    button[kind="primary"] {
        background-color: #d6336c !important;  /* pink/red */
        color: white !important;
        border: none;
        border-radius: 5px;
    }

    button[kind="secondary"] {
        background-color: #9c36b5 !important;  /* purple */
        color: white !important;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #f06595;  /* pinkish red */
    }

    /* Info boxes */
    .stAlert {
        border-left: 5px solid #9c36b5;  /* purple left border */
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Title
st.title("🎯 Number Guessing Game")

# Name input
name = st.text_input("👤 What's your name?", key="name")
if name:
    st.write(f"Welcome, **{name}**! 🎮")

# Range selection (locked after game starts)
disable_range = "comp_no" in st.session_state and not st.session_state.get("game_over", True)

col1, col2 = st.columns(2)
with col1:
    min_num = st.number_input("Min number", value=1, min_value=1, max_value=999, disabled=disable_range)
with col2:
    max_num = st.number_input("Max number", value=100, min_value=min_num + 1, max_value=1000, disabled=disable_range)

# Difficulty selection
difficulty = st.selectbox(
    "🎮 Choose difficulty:",
    ["Easy", "Medium", "Hard"],
    disabled=disable_range
)

# Max attempts based on difficulty
if difficulty == "Easy":
    max_attempts = 10
elif difficulty == "Medium":
    max_attempts = 6
else:
    max_attempts = 3

# Initialize session state
if "comp_no" not in st.session_state:
    st.session_state.comp_no = random.randint(min_num, max_num)
    st.session_state.attempts = 0
    st.session_state.max_attempts = max_attempts
    st.session_state.game_over = False
    st.session_state.hint_used = False
    st.session_state.min_num = min_num
    st.session_state.max_num = max_num
    st.session_state.leaderboard = []

# Update state if not game over
if not st.session_state.game_over:
    st.session_state.min_num = min_num
    st.session_state.max_num = max_num
    st.session_state.max_attempts = max_attempts

# Instructions
st.markdown(f"📝 **Guess between {st.session_state.min_num} and {st.session_state.max_num}.**")
st.markdown(f"❤️ You have **{st.session_state.max_attempts}** attempts.")

# Hint button
if not st.session_state.hint_used and not st.session_state.game_over:
    if st.button("🧠 Need a hint?"):
        hint_range = 5
        hint_lower = max(st.session_state.comp_no - hint_range, st.session_state.min_num)
        hint_upper = min(st.session_state.comp_no + hint_range, st.session_state.max_num)
        st.info(f"🔍 The number is between **{hint_lower}** and **{hint_upper}**.")
        st.session_state.hint_used = True

# Game input
if not st.session_state.game_over:
    user_guess = st.number_input("🎯 Your guess:", min_value=st.session_state.min_num, max_value=st.session_state.max_num, step=1)
    if st.button("🚀 Submit Guess"):
        st.session_state.attempts += 1
        comp_no = st.session_state.comp_no
        attempts = st.session_state.attempts
        max_attempts = st.session_state.max_attempts

        if user_guess == comp_no:
            st.success(f"🎉 Correct! The number was **{comp_no}**. You got it in {attempts} tries!")
            st.balloons()
            st.session_state.game_over = True
            st.session_state.leaderboard.append((name, attempts))
            st.session_state.leaderboard.sort(key=lambda x: x[1])
        elif attempts >= max_attempts:
            st.error(f"💥 Out of attempts! The number was **{comp_no}**.")
            st.session_state.game_over = True
        elif user_guess < comp_no:
            st.info("🔼 Try a **higher** number.")
        else:
            st.info("🔽 Try a **lower** number.")

        st.markdown(f"🔢 **Attempts used:** {attempts} / {max_attempts}")
else:
    if st.button("🔄 Restart Game"):
        st.session_state.comp_no = random.randint(st.session_state.min_num, st.session_state.max_num)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.hint_used = False
        st.experimental_rerun()

# Leaderboard
if st.session_state.get("leaderboard"):
    st.markdown("## 🏆 Leaderboard")
    for i, (player, score) in enumerate(st.session_state.leaderboard[:5], start=1):
        st.markdown(f"{i}. **{player}** — {score} tries")
