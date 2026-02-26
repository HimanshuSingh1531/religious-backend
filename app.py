from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pandas as pd
import random
import os
import re

# Semantic similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Spiritual Assistant Backend")

# ---------------- LOAD DATASET ----------------


df = pd.read_csv("realistic_spiritual_riddles.csv")

AUDIO_DIR = "audio"

# ---------------- TEXT CLEANING ----------------

PLACE_WORDS = r"\b(temple|mandir|church|mosque|gurudwara|dargah|ashram|location|place)\b"

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(PLACE_WORDS, "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    return text.strip()

# ---------------- SMART CORPUS ----------------

corpus = (
    df["answer"].apply(clean_text) + " " +
    df["hint"].apply(clean_text)
).tolist()

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2
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
    return {"status": "Spiritual Assistant running successfully"}

# ---------------- RELIGION DETECTION ----------------

def detect_religion(q: str):
    q = q.lower()
    if any(w in q for w in ["hindu", "ved", "gita", "krishna", "ram"]):
        return "hindu"
    if any(w in q for w in ["islam", "allah", "quran"]):
        return "islam"
    if any(w in q for w in ["christian", "jesus", "bible"]):
        return "christian"
    if "buddh" in q:
        return "buddhist"
    return None

# ---------------- EMOTION DETECTION ----------------

def detect_emotion(q: str):
    emotions = {
        "anxiety": ["anxiety", "anxious", "stress", "worried", "fear"],
        "sadness": ["sad", "lonely", "depressed", "hopeless"],
        "confusion": ["confused", "lost", "meaning", "purpose"]
    }
    for emotion, words in emotions.items():
        if any(w in q.lower() for w in words):
            return emotion
    return None

# ---------------- SPIRITUAL ASSISTANT ----------------

@app.post("/ask")
def ask_question(data: QuestionRequest):
    raw_q = data.question


    user_q = clean_text(raw_q)


    user_vec = vectorizer.transform([user_q])

    similarities = cosine_similarity(user_vec, tfidf_matrix)[0]


    best_idx = similarities.argmax()

    best_score = similarities[best_idx]

    religion = detect_religion(raw_q)
    emotion = detect_emotion(raw_q)

    # ---------- LOW CONFIDENCE : DATASET-DRIVEN FALLBACK ----------
    if best_score < 0.12:
        emotion_keywords = {
            "anxiety": ["peace", "mind", "fear", "attachment", "calm"],
            "sadness": ["suffering", "hope", "compassion", "pain"],
            "confusion": ["truth", "path", "wisdom", "self", "knowledge"]
        }

        if emotion and emotion in emotion_keywords:
            mask = df["answer"].str.contains(
                "|".join(emotion_keywords[emotion]),
                case=False,
                na=False
            )
            subset = df[mask]
            if not subset.empty:
                row = subset.sample(1).iloc[0]
                return {
                    "answer": row["answer"],
                    "religion": religion,
                    "difficulty": "reflection"
                }

        # ultimate fallback (still dataset based)
        row = df.sample(1).iloc[0]
        return {
            "answer": row["answer"],
            "religion": row.get("religion"),
            "difficulty": "reflection"
        }

    # ---------- HIGH CONFIDENCE : NORMAL MATCH ----------
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
            "book": "Derived from spiritual teachings"
        }

    row = subset.sample(1).iloc[0]

    if data.content_type == "Quote":
        text = row["answer"]

    elif data.content_type == "Short Story":
        text = f"Reflection:\n{row['hint']}\n\nWisdom:\n{row['answer']}"
    else:
        text = f"Spiritual Path:\n\n{row['answer']}"

    return {
        "text": text,
        "religion": data.religion,
        "book": "Derived from spiritual riddles"
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