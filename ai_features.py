import streamlit as st
import random
import re
import os
from llama_cpp import Llama
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from music_backend import load_library, get_songs_by_religion, get_audio_path

# ---------------- CONFIG ----------------
GGUF_MODEL_PATH = "tinyllama_lora_merged.gguf"

MAX_TOKENS_QUOTE = 60
MAX_TOKENS_STORY = 220
MAX_TOKENS_PATHWAY = 600

BELIEFS = {
    "Hinduism": ["Bhagavad Gita", "Upanishads", "Yoga Vasistha"],
    "Buddhism": ["Sutta Nipata", "Majjhima Nikaya"],
    "Jainism": ["Acaranga Sutra", "Samayasara"],
    "Christianity": ["Bible"],
    "Islam": ["Quran"],
    "Atheism": ["The Age of Reason", "Human Values"]
}

# ---------------- UI ----------------
st.set_page_config(page_title="Daily Wisdom", layout="centered")
st.title("🧘 Daily Wisdom Generator")
st.caption("Book-grounded philosophical content")

# ---------------- APP MODE ----------------
app_mode = st.sidebar.radio(
    "📂 Select App Mode",
    ["Daily Wisdom", "Devotional Music"]
)

# ---------------- DAILY WISDOM MODE ----------------
if app_mode == "Daily Wisdom":

    belief = st.selectbox("Select belief system", list(BELIEFS.keys()))
    content_type = st.radio("Select content type", ["Quote", "Short Story", "Pathway"])

    # ---------------- LOAD LLM ----------------
    @st.cache_resource(show_spinner=True)
    def load_model():
        return Llama(
            model_path=GGUF_MODEL_PATH,
            n_gpu_layers=8,
            n_batch=8
        )

    llm = load_model()

    # ---------------- LOAD TRANSLATOR ----------------
    @st.cache_resource(show_spinner=True)
    def load_translator():
        model_name = "facebook/nllb-200-distilled-600M"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return tokenizer, model

    translator_tokenizer, translator_model = load_translator()

    # ---------------- LANGUAGES ----------------
    LANGUAGES = {
        "English": "eng_Latn",
        "Hindi": "hin_Deva",
        "Tamil": "tam_Taml",
        "Telugu": "tel_Telu",
        "Kannada": "kan_Knda",
        "Malayalam": "mal_Mlym",
        "Bengali": "ben_Beng",
        "Gujarati": "guj_Gujr",
        "Marathi": "mar_Deva",
        "Punjabi": "pan_Guru",
        "Urdu": "urd_Arab"
    }

    selected_language = st.selectbox("🌍 Translate Output To", list(LANGUAGES.keys()))

    # ---------------- PROMPT ----------------
    def build_prompt(belief, book, content_type):
        if content_type == "Quote":
            return (
                f"Generate ONE philosophical quote inspired by {book} of {belief}. "
                f"Single sentence only. Deep and reflective."
            )
        
        elif content_type == "Short Story":
            return (
                f"Generate a short philosophical story inspired by {book} of {belief}. "
                f"3 to 5 sentences. Reflective and parable-like."
            )

        elif content_type == "Pathway":
            return (
                f"You are a traditional spiritual master.\n"
                f"Create a structured spiritual roadmap for attaining the highest spiritual goal "
                f"in {belief}, based strictly on teachings from {book}.\n\n"
                f"The roadmap must:\n"
                f"- Contain 6 to 8 numbered steps.\n"
                f"- Show spiritual progression from beginner to advanced level.\n"
                f"- Include real concepts, practices, or doctrines from {book}.\n"
                f"- End with the final spiritual realization (moksha, enlightenment, salvation, or divine union depending on the tradition).\n\n"
                f"Start from foundational discipline and move toward ultimate realization.\n"
                f"Number each step clearly from 1.\n"
                f"Do not give general moral advice. Focus on spiritual advancement.\n"
            )

    # ---------------- CLEAN OUTPUT ----------------
    def clean_output(text, content_type):
        text = text.strip()
        text = text.replace('"', '').replace("“", "").replace("”", "")
        text = re.sub(r"\s+", " ", text)

        if content_type in ["Quote", "Short Story"]:
            sentences = re.split(r'(?<=[.!?]) +', text)
            clean_sentences = [s.strip() for s in sentences if len(s.split()) > 5]
            if content_type == "Quote":
                return clean_sentences[0] + "." if clean_sentences else text
            return " ".join(clean_sentences[:5])

        if content_type == "Pathway":

            steps = re.findall(r'\d+\.\s(.*?)(?=\d+\.|$)', text)
            steps = [s.strip() for s in steps if len(s.split()) > 4]

            if len(steps) < 3:
                sentences = re.split(r'(?<=[.!?]) +', text)
                steps = [s.strip() for s in sentences if len(s.split()) > 6]

            # Remove incomplete last step
            if steps:
                last_step = steps[-1]
                if (
                    last_step.endswith("-") or
                    last_step.endswith("(") or
                    last_step.count("(") > last_step.count(")")
                ):
                    steps = steps[:-1]

            if not steps:
                return text.strip()

            steps = steps[:8]

            numbered = [f"{i}. {step}" for i, step in enumerate(steps, 1)]
            return "\n".join(numbered)

    # ---------------- GENERATE ----------------
    def generate_content(prompt, max_tokens, content_type):

        full_prompt = (
            "You are a wise spiritual philosopher.\n\n"
            + prompt +
            "\n\nAnswer:"
        )

        output = llm(
            full_prompt,
            max_tokens=max_tokens,
            temperature=0.35 if content_type == "Pathway" else 0.7
        )

        generated = output['choices'][0]['text']
        return clean_output(generated, content_type)

    # ---------------- TRANSLATE ----------------
    def translate_text(text, target_lang):

        if target_lang == "English":
            return text

        translator_tokenizer.src_lang = "eng_Latn"

        inputs = translator_tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        forced_bos_token_id = translator_tokenizer.convert_tokens_to_ids(
            LANGUAGES[target_lang]
        )

        translated_tokens = translator_model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=1024
        )

        return translator_tokenizer.decode(
            translated_tokens[0],
            skip_special_tokens=True
        )

    # ---------------- RUN ----------------
    if st.button("✨ Generate Wisdom"):

        book = random.choice(BELIEFS[belief])

        with st.spinner("Reflecting..."):
            prompt = build_prompt(belief, book, content_type)

            max_tokens = {
                "Quote": MAX_TOKENS_QUOTE,
                "Short Story": MAX_TOKENS_STORY,
                "Pathway": MAX_TOKENS_PATHWAY
            }[content_type]

            english_result = generate_content(prompt, max_tokens, content_type)
            translated_result = translate_text(english_result, selected_language)

        st.markdown("---")

        st.subheader("📖 English Version")
        st.text(english_result)

        if selected_language != "English":
            st.subheader(f"🌍 {selected_language} Translation")
            formatted_translation = re.sub(r'\s(\d+\.)', r'\n\1', translated_result)
            st.text(formatted_translation)

        st.caption(f"Source Tradition: {belief} • Book: {book}")

# ---------------- DEVOTIONAL MUSIC MODE ----------------
if app_mode == "Devotional Music":

    st.title("🎵 Devotional Music Platform")

    music_library = load_library()

    if not music_library:
        st.warning("No songs found inside audio folders.")
        st.stop()

    religion = st.selectbox("Select Religion", list(music_library.keys()))

    songs = get_songs_by_religion(religion)

    if not songs:
        st.info("No songs available in this folder.")
        st.stop()

    selected_song = st.selectbox("Choose a Song", songs)

    audio_path = get_audio_path(religion, selected_song)

    if audio_path and os.path.exists(audio_path):
        st.markdown(f"### 🎶 Now Playing: {selected_song}")
        audio_bytes = open(audio_path, "rb").read()
        st.audio(audio_bytes)
    else:
        st.error("File path mismatch. Check folder naming.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("AI Philosopher • GGUF + NLLB • Dual Language Output")