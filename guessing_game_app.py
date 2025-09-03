import streamlit as st
import random

st.title("🎯 Number Guessing Game")

# Ask for user name
name = st.text_input("What's your name?")
if name:
    st.write(f"Welcome, {name}!")

# Select difficulty
difficulty = st.selectbox("Choose difficulty:", ["Easy", "Medium", "Hard"])

# Set max attempts based on difficulty
if difficulty == "Easy":
    max_attempts = 10
elif difficulty == "Medium":
    max_attempts = 5
else:
    max_attempts = 3

# Store in session state if not already set
if "comp_no" not in st.session_state:
    st.session_state.comp_no = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.max_attempts = max_attempts
else:
    # Update max_attempts if difficulty is changed during the session
    st.session_state.max_attempts = max_attempts

# Display game instructions
st.write(f"Guess the number (between 1 and 100). You have {st.session_state.max_attempts} chances!")

# Main game logic
if not st.session_state.game_over:
    user_input = st.number_input("Enter your guess:", min_value=1, max_value=100, step=1)
    if st.button("Submit Guess"):
        st.session_state.attempts += 1
        comp_no = st.session_state.comp_no
        attempts = st.session_state.attempts
        max_attempts = st.session_state.max_attempts

        if user_input == comp_no:
            st.success(f"🎉 CONGRATS! You guessed the number in {attempts} tries!")
            st.session_state.game_over = True
        elif attempts >= max_attempts:
            st.error(f"💥 Game Over! The number was {comp_no}.")
            st.session_state.game_over = True
        elif user_input < comp_no:
            st.info("🔼 Try a HIGHER number.")
        else:
            st.info("🔽 Try a LOWER number.")

        st.write(f"{attempts} attempts used, {max_attempts - attempts} remaining.")
else:
    if st.button("Restart Game"):
        st.session_state.comp_no = random.randint(1, 100)
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.experimental_rerun()
