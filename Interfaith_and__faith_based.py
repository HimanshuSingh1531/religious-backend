
# =========================================
# Streamlit App: AI Philosopher (GGUF FINAL STABLE)
# =========================================

import streamlit as st
import random
import pandas as pd
from llama_cpp import Llama

# -----------------------------------------
# CONFIG
# -----------------------------------------
MODEL_PATH = "tinyllama_lora_merged.gguf"
MAX_NEW_TOKENS = 70

# -----------------------------------------
# BELIEF SYSTEMS
# -----------------------------------------
BELIEFS = {
    "Hinduism": ["Bhagavad Gita", "Upanishads", "Ramayana"],
    "Buddhism": ["Majjhima Nikaya", "Sutta Nipata"],
    "Jainism": ["Acaranga Sutra", "Samayasara"],
    "Christianity": ["Bible"],
    "Islam": ["Quran"],
    "Atheism": ["The Age of Reason", "Human Values"]
}

# -----------------------------------------
# UI SETUP
# -----------------------------------------
st.set_page_config(page_title="AI Philosopher", layout="centered")
st.title("🧘 AI Philosopher")
st.caption("Book-grounded wisdom only • No hallucinations")

# ---- CSS FIX FOR TABLE WRAPPING ----
st.markdown("""
<style>
    .stDataFrame td {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        vertical-align: top;
    }
</style>
""", unsafe_allow_html=True)

mode = st.radio(
    "Select mode",
    [
        "Single Belief Answer",
        "Multi-Belief Comparison (Table)",
        "Theism vs Atheism (Table)"
    ]
)

question = st.text_area(
    "Ask your real-life question:",
    "Why do humans feel anxious about the future?",
    height=120
)

# -----------------------------------------
# SELECTION
# -----------------------------------------
if mode == "Single Belief Answer":
    selected_beliefs = [st.selectbox("Select belief system", list(BELIEFS.keys()))]

elif mode == "Multi-Belief Comparison (Table)":
    all_beliefs = [b for b in BELIEFS if b != "Atheism"]
    selected_beliefs = st.multiselect(
        "Select belief systems",
        all_beliefs,
        default=all_beliefs
    )

else:
    theism = st.selectbox(
        "Select theistic tradition",
        [b for b in BELIEFS if b != "Atheism"]
    )

# -----------------------------------------
# LOAD GGUF MODEL
# -----------------------------------------
@st.cache_resource
def load_model():
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=8,      # Adjust based on CPU cores
        n_gpu_layers=0    # Set >0 if GPU offloading supported
    )
    return llm

llm = load_model()

# -----------------------------------------
# GENERATION
# -----------------------------------------
def generate(prompt):
    output = llm(
        prompt,
        max_tokens=MAX_NEW_TOKENS,
        temperature=0.25,
        top_p=0.85,
        repeat_penalty=1.25,
        stop=["Question:", "\n\n"]
    )

    text = output["choices"][0]["text"].strip()
    text = text.replace("\n", " ")
    sentences = text.split(". ")
    return ". ".join(sentences[:2]).strip() + "."

def build_prompt(belief, book, question):
    return f"""
You are a calm philosophical thinker representing {belief}.
Base your reasoning only on the philosophical themes found in {book}.

STRICT RESPONSE RULES:

1. EXACTLY 2 sentences.
2. Calm, emotionally neutral tone.
3. No defense of any religion.
4. No criticism of any religion.
5. No superiority claims.
6. Do not justify hate.
7. Do not attack or support any belief.
8. Do not describe historical facts.
9. Do not repeat aggressive wording from the question.
10. Focus only on inner psychological and philosophical insight.

If the question expresses anger, rejection, or hatred, interpret it as a reflection of inner conflict and respond with wisdom about understanding, awareness, and self-examination.

Question:
{question}

Answer:
"""

# -----------------------------------------
# RUN
# -----------------------------------------
if st.button("✨ Ask Philosopher"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    st.markdown("---")

    # ---------- SINGLE ----------
    if mode == "Single Belief Answer":
        belief = selected_beliefs[0]
        book = random.choice(BELIEFS[belief])

        with st.spinner("Thinking..."):
            ans = generate(build_prompt(belief, book, question))

        st.markdown(f"### 🕊 {belief}")
        st.write(ans)
        st.caption(f"Source Book: {book}")

    # ---------- MULTI TABLE ----------
    elif mode == "Multi-Belief Comparison (Table)":

        rows = []
        for belief in selected_beliefs:
            book = random.choice(BELIEFS[belief])

            with st.spinner(f"{belief} thinking..."):
                ans = generate(build_prompt(belief, book, question))

            rows.append({
                "Belief System": belief,
                "Answer": ans,
                "Source Book": book
            })

        df = pd.DataFrame(rows)

        st.subheader("📊 Multi-Belief Comparison")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # ---------- THEISM vs ATHEISM ----------
    else:
        t_book = random.choice(BELIEFS[theism])
        a_book = random.choice(BELIEFS["Atheism"])

        with st.spinner("Comparing views..."):
            t_ans = generate(build_prompt(theism, t_book, question))
            a_ans = generate(build_prompt("Atheism", a_book, question))

        df = pd.DataFrame([
            {"Belief System": theism, "Answer": t_ans, "Source Book": t_book},
            {"Belief System": "Atheism", "Answer": a_ans, "Source Book": a_book}
        ])

        st.subheader("📊 Theism vs Atheism Comparison")
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("---")
st.caption("Stable AI Philosopher • Table-based comparison • No synthesis")     