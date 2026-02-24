from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pandas as pd
import random
import os

# 🔥 Semantic similarity (GPT-like logic)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Religious Q&A Backend")

# ---------------- LOAD DATASET ----------------

df = pd.read_csv("realistic_spiritual_riddles.csv")

AUDIO_DIR = "audio"

# ---------------- SEMANTIC SEARCH SETUP ----------------
# Wisdom + context (NOT temple focused)

corpus = (
    
    df["answer"].fillna("") + " " +
    df["hint"].fillna("") + " " +
    df["religion"].fillna("")
).tolist()

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)
tfidf_matrix = vectorizer.fit_transform(corpus)

# ---------------- REQUEST MODELS ----------------

class QuestionRequest(BaseModel):
    question: str


class WisdomRequest(BaseModel):
    religion: str
    content_type: str


class SubmitAnswerRequest(BaseModel):
    user_answer: str
    correct_answer: str
    points: int


# ---------------- ROOT ----------------

@app.get("/")
def root():
    return {"status": "Backend running successfully"}

# ---------------- HELPER: RELIGION DETECTION ----------------

def detect_religion_from_question(q: str):
    q = q.lower()
    if "hindu" in q:
        return "hindu"
    if "islam" in q or "muslim" in q:
        return "islam"
    if "christian" in q or "jesus" in q:
        return "christian"
    if "buddh" in q:
        return "buddhist"
    return None

# ---------------- ASK QUESTION (SMART + DATASET ONLY) ----------------

@app.post("/ask")
def ask_question(data: QuestionRequest):
    user_q = data.question.lower()

    # Vectorize user question
    user_vec = vectorizer.transform([user_q])

    similarities = cosine_similarity(user_vec, tfidf_matrix)[0]

    # Base best match
    best_idx = similarities.argmax()
    best_score = similarities[best_idx]

    # Religion-aware refinement
    detected_religion = detect_religion_from_question(user_q)
    if detected_religion:
        religion_subset = df[
            df["religion"].str.lower().str.contains(detected_religion, na=False)
        ]
        if not religion_subset.empty:
            # recompute similarity inside religion subset
            sub_corpus = (
                religion_subset["answer"].fillna("") + " " +
                religion_subset["hint"].fillna("")
            ).tolist()
            sub_matrix = vectorizer.transform(sub_corpus)
            sub_sim = cosine_similarity(user_vec, sub_matrix)[0]
            row = religion_subset.iloc[sub_sim.argmax()]
        else:
            row = df.iloc[best_idx]
    else:
        # generic semantic match
        if best_score < 0.05:
            row = df.sample(1).iloc[0]
        else:
            row = df.iloc[best_idx]

    return {
        "answer": row["answer"],
        "religion": row.get("religion"),

        "difficulty": row.get("difficulty")
    }

# ---------------- REAL WISDOM ----------------

@app.post("/wisdom")
def generate_wisdom(data: WisdomRequest):

    subset = df[df["religion"].str.lower() == data.religion.lower()]

    if subset.empty:
        row = df.sample(1).iloc[0]
        return {
            "text": row["answer"],
            "religion": row.get("religion"),
            "book": "Derived from authentic scriptures"
        }

    row = subset.sample(1).iloc[0]

    if data.content_type == "Quote":
        text = row["answer"]

    elif data.content_type == "Short Story":

        text = (

            f"Reflection:\n{row['hint']}\n\n"
            f"Wisdom:\n{row['answer']}"
        )

    else:  # Pathway
        text = f"Spiritual Path:\n\n{row['answer']}"

    return {
        "text": text,
        "religion": data.religion,
        "book": "Derived from authentic religious riddles"
    }

# ---------------- RIDDLE GAME ----------------

@app.get("/riddle")
def get_riddle():
    row = df.sample(1).iloc[0]
    return {
        "riddle": row["riddle"],
        "hint": row["hint"],
        "answer": row["answer"],
        "points": int(row["points"])
    }

# ---------------- SUBMIT ANSWER ----------------

@app.post("/submit")
def submit_answer(data: SubmitAnswerRequest):
    if data.user_answer.strip().lower() == data.correct_answer.strip().lower():
        return {"correct": True, "earned_points": data.points}
    return {"correct": False, "earned_points": 0}

# ---------------- MUSIC APIs ----------------

@app.get("/music/{religion}")
def list_music(religion: str):
    folder = os.path.join(AUDIO_DIR, religion)

    if not os.path.exists(folder):
        return []
    
    return os.listdir(folder)


@app.get("/play/{religion}/{song}")
def play_music(religion: str, song: str):
    file_path = os.path.join(AUDIO_DIR, religion, song)

    if not os.path.exists(file_path):
        return {"error": "File not found"}
    
    return FileResponse(file_path, media_type="audio/mpeg")