import os

AUDIO_ROOT = "audio"

# -------- LOAD RELIGION FOLDERS --------
def load_library():
    """
    Returns dictionary:
    {
        "Hinduism": ["song1.mp3", "song2.mp3"],
        "Christianity": ["song1.mp3"]
    }
    """
    library = {}

    if not os.path.exists(AUDIO_ROOT):
        return library

    for religion in os.listdir(AUDIO_ROOT):
        religion_path = os.path.join(AUDIO_ROOT, religion)

        if os.path.isdir(religion_path):
            songs = [
                f for f in os.listdir(religion_path)
                if f.endswith(".mp3")
            ]
            library[religion.capitalize()] = songs

    return library


def get_songs_by_religion(religion_name):
    """
    Returns list of songs for selected religion
    """
    library = load_library()
    return library.get(religion_name.capitalize(), [])


def get_audio_path(religion_name, song_name):
    """
    Returns full path of selected song
    """
    return os.path.join(
        AUDIO_ROOT,
        religion_name.lower(),
        song_name
    )


# -------- Example Usage --------
if __name__ == "__main__":
    library = load_library()

    if not library:
        print("No songs found.")
    else:
        print("Available Religions:")
        for r in library:
            print("-", r)

        religion = input("Select religion: ")
        songs = get_songs_by_religion(religion)

        if songs:
            print("Songs:")
            for s in songs:
                print("-", s)

            song = input("Select song: ")
            path = get_audio_path(religion, song)

            if os.path.exists(path):
                print("Playing file path:", path)
            else:
                print("File not found.")
        else:
            print("No songs available.")