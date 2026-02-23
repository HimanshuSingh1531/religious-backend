from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pandas as pd
import random
import os

app = FastAPI(title="Religious Q&A Backend")

# ---------------- LOAD DATASET ----------------

df = pd.read_csv("realistic_spiritual_riddles.csv")

AUDIO_DIR = "audio"

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

# ---------------- ASK QUESTION ----------------

@app.post("/ask")
def ask_question(data: QuestionRequest):
    user_q = data.question.lower()

    for _, row in df.iterrows():
        if user_q in str(row["riddle"]).lower():
            return {
                "answer": row["answer"],
                "religion": row["religion"],
                "landmark": row["landmark"],
                "difficulty": row["difficulty"]
            }

    return {
        "answer": "No matching answer found in the scriptures.",
        "religion": None,
        "landmark": None,
        "difficulty": None
    }

# ---------------- REAL WISDOM ----------------

@app.post("/wisdom")
def generate_wisdom(data: WisdomRequest):

    subset = df[df["religion"].str.lower() == data.religion.lower()]

    if subset.empty:
        return {
            "text": "No wisdom found for the selected tradition.",
            "religion": data.religion,
            "book": None
        }

    subset = subset.sample(min(5, len(subset)))

    if data.content_type == "Quote":
        text = subset.iloc[0]["answer"]

    elif data.content_type == "Short Story":
        row = subset.iloc[0]
        text = (
            f"A seeker once pondered:\n\n"
            f"{row['riddle']}\n\n"
            f"Reflection:\n{row['hint']}\n\n"
            f"Wisdom:\n{row['answer']}"
        )

    else:  # Pathway
        steps = [
            f"{i+1}. {row['answer']}"
            for i, (_, row) in enumerate(subset.iterrows())
        ]
        text = "Spiritual Pathway:\n\n" + "\n".join(steps)

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


@app.post("/submit")
def submit_answer(data: SubmitAnswerRequest):
    if data.user_answer.strip().lower() == data.correct_answer.strip().lower():
        return {
            "correct": True,
            "earned_points": data.points
        }

    return {
        "correct": False,
        "earned_points": 0
    }

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