import streamlit as st
import pandas as pd
import random

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="🌿 Spiritual Riddle Journey", layout="centered")

st.title("🌿 Spiritual Riddle Journey")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("realistic_spiritual_riddles.csv")

df = load_data()

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "current_riddle" not in st.session_state:
    st.session_state.current_riddle = df.sample(1).iloc[0]

if "show_hint" not in st.session_state:
    st.session_state.show_hint = False

# ------------------------------------------------
# USER NAME
# ------------------------------------------------
name = st.text_input("Enter Your Name", value="Moorthy")

if name:
    st.subheader(f"🌿 Welcome {name}")

# ------------------------------------------------
# SCOREBOARD
# ------------------------------------------------
col1, col2 = st.columns(2)

col1.metric("⭐ XP", st.session_state.xp)
col2.metric("🔥 Streak", f"{st.session_state.streak} correct")

st.divider()

# ------------------------------------------------
# DISPLAY RIDDLE
# ------------------------------------------------
riddle_data = st.session_state.current_riddle

st.markdown("### 🧠 Riddle")
st.write(riddle_data["riddle"])

# ------------------------------------------------
# HINT BUTTON
# ------------------------------------------------
if st.button("💡 Show Hint"):
    st.session_state.show_hint = True

if st.session_state.show_hint:
    st.info(riddle_data["hint"])

# ------------------------------------------------
# ANSWER INPUT
# ------------------------------------------------
user_answer = st.text_input("Your Answer")

if st.button("Submit Answer"):

    correct_answer = riddle_data["answer"].strip().lower()
    user_answer_clean = user_answer.strip().lower()

    if user_answer_clean == correct_answer:
        st.success("✅ Correct! Well done.")

        st.session_state.xp += int(riddle_data["points"])
        st.session_state.streak += 1

        # Load new riddle
        st.session_state.current_riddle = df.sample(1).iloc[0]
        st.session_state.show_hint = False

    else:
        st.error(f"❌ Incorrect! The correct answer was: {riddle_data['landmark']}")
        st.session_state.streak = 0

st.divider()

# ------------------------------------------------
# NEXT RIDDLE BUTTON
# ------------------------------------------------
if st.button("🎮 Skip Riddle"):
    st.session_state.current_riddle = df.sample(1).iloc[0]
    st.session_state.show_hint = False

# ------------------------------------------------
# LEVEL SYSTEM
# ------------------------------------------------
st.divider()

if st.session_state.xp < 50:
    level = "Seeker"
elif st.session_state.xp < 150:
    level = "Explorer"
elif st.session_state.xp < 300:
    level = "Pilgrim"
else:
    level = "Spiritual Master"

st.subheader(f"🏆 Title: {level}")