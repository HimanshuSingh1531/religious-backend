import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import geocoder

# ---------------- CONFIG ----------------
CSV_FILE = "india_religious_landmarks_phase1_full.csv"
st.set_page_config(page_title="India Religious Landmarks Planner", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(CSV_FILE)
df['religion'] = df['religion'].str.strip().str.title()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filter Landmarks")
religions = sorted(df["religion"].unique())
states = sorted(df["state"].unique())

selected_religion = st.sidebar.selectbox("Select Religion", ["All"] + religions)
selected_state = st.sidebar.selectbox("Select State", ["All"] + states)

# ---------------- USER LOCATION ----------------
g = geocoder.ip('me')
if g.ok:
    user_lat, user_lon = g.latlng
else:
    user_lat, user_lon = 20.5937, 78.9629

st.sidebar.write(f"Detected Location: {user_lat:.4f}, {user_lon:.4f}")

# ---------------- FILTER DATA ----------------
filtered = df.copy()

if selected_religion != "All":
    filtered = filtered[filtered["religion"] == selected_religion]

if selected_state != "All":
    filtered = filtered[filtered["state"] == selected_state]

# ---------------- DISTANCE CALCULATION ----------------
def calc_distance(row):
    return geodesic((user_lat, user_lon), (row["latitude"], row["longitude"])).km

if not filtered.empty:
    filtered["distance_km"] = filtered.apply(calc_distance, axis=1)
    filtered = filtered.sort_values("distance_km")

# ---------------- UI ----------------
st.title("🕌 India Religious Landmarks Planner")

st.subheader("🏛 Landmark List")
for _, row in filtered.iterrows():
    st.markdown(f"### {row['name']}")
    st.write(f"**Religion:** {row['religion']} | **State:** {row['state']} | **City:** {row['city']}")
    st.write(f"**Distance:** {row['distance_km']:.2f} km")
    st.markdown("---")

# ---------------- ITINERARY SETTINGS ----------------
st.subheader("🤖 AI Travel Itinerary Generator")
num_days = st.selectbox("Select Number of Days", [1, 2, 3, 4, 5])

itinerary_mode = st.radio(
    "Itinerary Mode",
    ["Auto AI Itinerary", "Manual Landmark Selection"]
)

if "itinerary" not in st.session_state:
    st.session_state.itinerary = {}

# =========================================================
# MANUAL MODE
# =========================================================
if itinerary_mode == "Manual Landmark Selection":

    selected_landmarks = st.multiselect(
        "Select Landmarks",
        options=filtered["name"].tolist()
    )

    generate_button = st.button("Generate Itinerary")

    if generate_button:

        if not selected_landmarks:
            st.warning("Please select at least one landmark.")
        else:
            remaining = filtered[filtered["name"].isin(selected_landmarks)].copy()
            day_itinerary = {}
            current_location = (user_lat, user_lon)

            for day in range(1, num_days + 1):

                if remaining.empty:
                    break

                # Find nearest from current location
                remaining["temp_distance"] = remaining.apply(
                    lambda row: geodesic(
                        current_location,
                        (row["latitude"], row["longitude"])
                    ).km,
                    axis=1
                )

                nearest = remaining.sort_values("temp_distance").iloc[0]

                day_itinerary[f"Day {day}"] = {
                    "start": current_location,
                    "place": nearest
                }

                current_location = (
                    nearest["latitude"],
                    nearest["longitude"]
                )

                remaining = remaining[remaining["name"] != nearest["name"]]

            st.session_state.itinerary = day_itinerary

# =========================================================
# AUTO MODE
# =========================================================
else:

    generate_button = st.button("Generate Itinerary")

    if generate_button:

        if filtered.empty:
            st.warning("No landmarks available.")
        else:
            remaining = filtered.copy()
            day_itinerary = {}
            current_location = (user_lat, user_lon)

            for day in range(1, num_days + 1):

                if remaining.empty:
                    break

                remaining["temp_distance"] = remaining.apply(
                    lambda row: geodesic(
                        current_location,
                        (row["latitude"], row["longitude"])
                    ).km,
                    axis=1
                )

                nearest = remaining.sort_values("temp_distance").iloc[0]

                day_itinerary[f"Day {day}"] = {
                    "start": current_location,
                    "place": nearest
                }

                current_location = (
                    nearest["latitude"],
                    nearest["longitude"]
                )

                remaining = remaining[remaining["name"] != nearest["name"]]

            st.session_state.itinerary = day_itinerary

# =========================================================
# DISPLAY ITINERARY
# =========================================================
if st.session_state.itinerary:

    for day, data in st.session_state.itinerary.items():

        st.markdown(f"## {day}")

        place = data["place"]
        start_location = data["start"]

        st.write(f"🏛 {place['name']} ({place['city']}, {place['state']})")

        route = [
            [start_location[0], start_location[1]],
            [place["latitude"], place["longitude"]]
        ]

        day_map = folium.Map(location=route[0], zoom_start=6)
        day_map.fit_bounds(route)

        # Start marker
        folium.Marker(
            route[0],
            popup="Start Location",
            icon=folium.Icon(color="red")
        ).add_to(day_map)

        # Destination marker
        folium.Marker(
            route[1],
            popup=place["name"],
            icon=folium.Icon(color="blue")
        ).add_to(day_map)

        # Route line
        folium.PolyLine(route, color="green", weight=3).add_to(day_map)

        st_folium(day_map, width=700, height=500)

    st.success("✅ Itinerary Generated Successfully!")