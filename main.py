from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from enum import Enum
from typing import Optional, List
import pandas as pd
import random
import math
import os

# ==========================================
# IMPORT AI MODULES
# ==========================================
import Interfaith_and__faith_based as philosopher
import ai_features as wisdom

app = FastAPI(title="Religious AI Unified Backend", version="2.0")

# ==================================================
# LOAD DATASETS SAFELY
# ==================================================

def load_csv_safe(path):
    try:
        df = pd.read_csv(path)
        df = df.replace([float("inf"), -float("inf")], None)
        df = df.fillna("")
        return df
    except:
        return pd.DataFrame()

landmarks_df = load_csv_safe("india_religious_landmarks_phase1.csv")
food_df = load_csv_safe("food_dataset.csv")
riddles_df = load_csv_safe("realistic_spiritual_riddles.csv")

# ==================================================
# ENUMS (Dropdowns)
# ==================================================

class ReligionEnum(str, Enum):
    All = "All"
    Hindu = "Hindu"
    Muslim = "Muslim"
    Christian = "Christian"
    Sikh = "Sikh"
    Buddhist = "Buddhist"
    Jain = "Jain"

class StateEnum(str, Enum):
    All = "All"
    TamilNadu = "Tamil Nadu"
    Kerala = "Kerala"
    Karnataka = "Karnataka"
    Delhi = "Delhi"
    Maharashtra = "Maharashtra"

class DietTypeEnum(str, Enum):
    Vegetarian = "Vegetarian"
    NonVegetarian = "Non-Vegetarian"

class GenderEnum(str, Enum):
    Male = "Male"
    Female = "Female"

class ActivityEnum(str, Enum):
    Sedentary = "Sedentary"
    Light = "Light"
    Moderate = "Moderate"
    Active = "Active"

class PhilosopherModeEnum(str, Enum):
    Single = "Single Belief Answer"
    Multi = "Multi Belief Answer"
    Compare = "Theism vs Atheism"

class ContentTypeEnum(str, Enum):
    Quote = "Quote"
    ShortStory = "Short Story"
    Pathway = "Pathway"

class LanguageEnum(str, Enum):
    English = "English"
    Tamil = "Tamil"
    Hindi = "Hindi"
    Malayalam = "Malayalam"

# ==================================================
# SAFE JSON CLEANER
# ==================================================

def clean_value(v):
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            return 0
        return float(v)
    return v

def clean_records(records):
    return [{k: clean_value(v) for k, v in row.items()} for row in records]

# ==================================================
# 🧘 AI PHILOSOPHER
# ==================================================

@app.get("/ask_philosopher")
def ask_philosopher(
    question: str,
    mode: PhilosopherModeEnum = PhilosopherModeEnum.Single,
    beliefs: Optional[List[ReligionEnum]] = Query(None)
):
    if not beliefs:
        beliefs = [ReligionEnum.Hindu]

    results = []

    for belief in beliefs:
        if belief.value == "All":
            continue

        book = random.choice(philosopher.BELIEFS.get(belief.value, []))
        prompt = philosopher.build_prompt(belief.value, book, question)
        ans = philosopher.generate(prompt)

        results.append({
            "belief": belief.value,
            "book": book,
            "answer": ans
        })

    return {"question": question, "results": results}

# ==================================================
# 📜 DAILY WISDOM
# ==================================================

@app.get("/daily_wisdom")
def daily_wisdom(
    religion: ReligionEnum,
    content_type: ContentTypeEnum = ContentTypeEnum.Quote,
    language: LanguageEnum = LanguageEnum.English
):
    book = random.choice(wisdom.BELIEFS.get(religion.value, []))
    prompt = wisdom.build_prompt(religion.value, book, content_type.value)

    max_tokens = {
        "Quote": wisdom.MAX_TOKENS_QUOTE,
        "Short Story": wisdom.MAX_TOKENS_STORY,
        "Pathway": wisdom.MAX_TOKENS_PATHWAY
    }[content_type.value]

    english_result = wisdom.generate_content(prompt, max_tokens, content_type.value)
    translated_result = wisdom.translate_text(english_result, language.value)

    return {
        "religion": religion.value,
        "book": book,
        "english": english_result,
        "translated": translated_result
    }

# ==================================================
# 🎵 DEVOTIONAL MUSIC
# ==================================================

@app.get("/music/list_religions")
def list_religions():
    library = wisdom.load_library()
    return {"religions": list(library.keys())}

@app.get("/music/list_songs")
def list_songs(religion: ReligionEnum):
    songs = wisdom.get_songs_by_religion(religion.value)
    return {"religion": religion.value, "songs": songs}

@app.get("/music/play")
def play_song(religion: ReligionEnum, song_name: str):
    path = wisdom.get_audio_path(religion.value, song_name)
    if path and os.path.exists(path):
        return FileResponse(path, media_type="audio/mpeg")
    return {"error": "File not found"}

# ==================================================
# 🕌 LANDMARKS API
# ==================================================

@app.get("/landmarks")
def get_landmarks(
    religion: ReligionEnum = ReligionEnum.All,
    state: StateEnum = StateEnum.All
):
    if landmarks_df.empty:
        return {"message": "Landmark dataset not loaded"}

    df = landmarks_df.copy()

    if religion != ReligionEnum.All:
        df = df[df["religion"] == religion.value]

    if state != StateEnum.All:
        df = df[df["state"] == state.value]

    if df.empty:
        return {"message": "No landmarks found"}

    return clean_records(df.head(50).to_dict(orient="records"))

# ==================================================
# 🥗 DIET API
# ==================================================

ACTIVITY_MULTIPLIER = {
    "Sedentary": 1.2,
    "Light": 1.375,
    "Moderate": 1.55,
    "Active": 1.725,
}

PROTEIN_PER_KG = 1.2

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    return 10 * weight + 6.25 * height - 5 * age - 161

@app.get("/diet")
def generate_diet(
    religion: ReligionEnum,
    diet_type: DietTypeEnum,
    age: int,
    gender: GenderEnum,
    weight: float,
    height: float,
    activity: ActivityEnum
):
    if food_df.empty:
        return {"message": "Food dataset not loaded"}

    df = food_df[
        (food_df["religion"] == religion.value) |
        (food_df["religion"] == "All")
    ]

    if diet_type == DietTypeEnum.Vegetarian:
        df = df[df["type"] == "veg"]
    else:
        df = df[df["type"] == "non-veg"]

    if df.empty:
        return {"message": "No food available"}

    bmr = calculate_bmr(weight, height, age, gender.value)
    calorie_target = int(bmr * ACTIVITY_MULTIPLIER[activity.value])
    protein_target = round(weight * PROTEIN_PER_KG, 1)

    selected = df.sample(n=min(6, len(df)))

    return {
        "calorie_target": calorie_target,
        "protein_target": protein_target,
        "meals": selected["name"].tolist(),
        "total_calories": int(selected["calories"].astype(float).sum()),
        "total_protein": round(selected["protein_g"].astype(float).sum(), 1)
    }

# ==================================================
# 🌿 RIDDLE API
# ==================================================

@app.get("/riddle")
def get_riddle():
    if riddles_df.empty:
        return {"message": "Riddle dataset not loaded"}

    r = riddles_df.sample(1).iloc[0]

    return {
        "riddle": str(r.get("riddle", "")),
        "hint": str(r.get("hint", "")),
        "points": int(clean_value(r.get("points", 0)))
    }

# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():
    return {"message": "Religious AI Backend Running Successfully 🚀"}