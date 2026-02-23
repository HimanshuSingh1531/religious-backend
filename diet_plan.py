import pandas as pd

# Complete list of 100 religious landmarks with basic info
landmarks = [
    # HINDU (40)
    {"name": "Kashi Vishwanath Temple", "religion": "Hindu", "state": "Uttar Pradesh", "city": "Varanasi"},
    {"name": "Tirumala Venkateswara Temple", "religion": "Hindu", "state": "Andhra Pradesh", "city": "Tirumala"},
    {"name": "Meenakshi Amman Temple", "religion": "Hindu", "state": "Tamil Nadu", "city": "Madurai"},
    {"name": "Badrinath Temple", "religion": "Hindu", "state": "Uttarakhand", "city": "Badrinath"},
    {"name": "Kedarnath Temple", "religion": "Hindu", "state": "Uttarakhand", "city": "Kedarnath"},
    {"name": "Jagannath Temple", "religion": "Hindu", "state": "Odisha", "city": "Puri"},
    {"name": "Ramanathaswamy Temple", "religion": "Hindu", "state": "Tamil Nadu", "city": "Rameswaram"},
    {"name": "Somnath Temple", "religion": "Hindu", "state": "Gujarat", "city": "Veraval"},
    {"name": "Mahakaleshwar Temple", "religion": "Hindu", "state": "Madhya Pradesh", "city": "Ujjain"},
    {"name": "Vaishno Devi Temple", "religion": "Hindu", "state": "Jammu & Kashmir", "city": "Katra"},
    {"name": "Sabarimala Temple", "religion": "Hindu", "state": "Kerala", "city": "Pathanamthitta"},
    {"name": "Dwarkadhish Temple", "religion": "Hindu", "state": "Gujarat", "city": "Dwarka"},
    {"name": "Akshardham Temple", "religion": "Hindu", "state": "Delhi", "city": "Delhi"},
    {"name": "Konark Sun Temple", "religion": "Hindu", "state": "Odisha", "city": "Konark"},
    {"name": "Kamakhya Temple", "religion": "Hindu", "state": "Assam", "city": "Guwahati"},
    {"name": "Shirdi Sai Baba Temple", "religion": "Hindu", "state": "Maharashtra", "city": "Shirdi"},
    {"name": "Padmanabhaswamy Temple", "religion": "Hindu", "state": "Kerala", "city": "Thiruvananthapuram"},
    {"name": "Lingaraj Temple", "religion": "Hindu", "state": "Odisha", "city": "Bhubaneswar"},
    {"name": "Brihadeeswarar Temple", "religion": "Hindu", "state": "Tamil Nadu", "city": "Thanjavur"},
    {"name": "Ayodhya Ram Mandir", "religion": "Hindu", "state": "Uttar Pradesh", "city": "Ayodhya"},
    {"name": "Trimbakeshwar Temple", "religion": "Hindu", "state": "Maharashtra", "city": "Nashik"},
    {"name": "Omkareshwar Temple", "religion": "Hindu", "state": "Madhya Pradesh", "city": "Omkareshwar"},
    {"name": "Bhimashankar Temple", "religion": "Hindu", "state": "Maharashtra", "city": "Pune"},
    {"name": "Guruvayur Temple", "religion": "Hindu", "state": "Kerala", "city": "Guruvayur"},
    {"name": "Udupi Sri Krishna Temple", "religion": "Hindu", "state": "Karnataka", "city": "Udupi"},
    {"name": "Kalighat Temple", "religion": "Hindu", "state": "West Bengal", "city": "Kolkata"},
    {"name": "Banke Bihari Temple", "religion": "Hindu", "state": "Uttar Pradesh", "city": "Vrindavan"},
    {"name": "Har Ki Pauri", "religion": "Hindu", "state": "Uttarakhand", "city": "Haridwar"},
    {"name": "Chidambaram Nataraja Temple", "religion": "Hindu", "state": "Tamil Nadu", "city": "Chidambaram"},
    {"name": "Virupaksha Temple", "religion": "Hindu", "state": "Karnataka", "city": "Hampi"},
    {"name": "Sringeri Sharada Peetham", "religion": "Hindu", "state": "Karnataka", "city": "Sringeri"},
    {"name": "Kollur Mookambika Temple", "religion": "Hindu", "state": "Karnataka", "city": "Kollur"},
    {"name": "Chottanikkara Temple", "religion": "Hindu", "state": "Kerala", "city": "Chottanikkara"},
    {"name": "Annavaram Temple", "religion": "Hindu", "state": "Andhra Pradesh", "city": "Annavaram"},
    {"name": "Parvati Temple", "religion": "Hindu", "state": "Maharashtra", "city": "Pune"},
    {"name": "Mangaladevi Temple", "religion": "Hindu", "state": "Karnataka", "city": "Mangalore"},
    {"name": "ISKCON Temple Bangalore", "religion": "Hindu", "state": "Karnataka", "city": "Bangalore"},
    {"name": "Rajarani Temple", "religion": "Hindu", "state": "Odisha", "city": "Bhubaneswar"},
    {"name": "Kanchi Kailasanathar Temple", "religion": "Hindu", "state": "Tamil Nadu", "city": "Kanchipuram"},
    {"name": "Chamundeshwari Temple", "religion": "Hindu", "state": "Karnataka", "city": "Mysore"},

    # MUSLIM (15)
    {"name": "Ajmer Sharif Dargah", "religion": "Muslim", "state": "Rajasthan", "city": "Ajmer"},
    {"name": "Jama Masjid", "religion": "Muslim", "state": "Delhi", "city": "Delhi"},
    {"name": "Haji Ali Dargah", "religion": "Muslim", "state": "Maharashtra", "city": "Mumbai"},
    {"name": "Charminar", "religion": "Muslim", "state": "Telangana", "city": "Hyderabad"},
    {"name": "Hazrat Nizamuddin Dargah", "religion": "Muslim", "state": "Delhi", "city": "Delhi"},
    {"name": "Mecca Masjid", "religion": "Muslim", "state": "Telangana", "city": "Hyderabad"},
    {"name": "Taj-ul-Masajid", "religion": "Muslim", "state": "Madhya Pradesh", "city": "Bhopal"},
    {"name": "Dargah of Salim Chishti", "religion": "Muslim", "state": "Rajasthan", "city": "Fatehpur Sikri"},
    {"name": "Tipu Sultan Mosque", "religion": "Muslim", "state": "Karnataka", "city": "Bangalore"},
    {"name": "Makkah Masjid", "religion": "Muslim", "state": "Telangana", "city": "Hyderabad"},
    {"name": "Raza Mosque", "religion": "Muslim", "state": "Uttar Pradesh", "city": "Rampur"},
    {"name": "Bara Imambara", "religion": "Muslim", "state": "Uttar Pradesh", "city": "Lucknow"},
    {"name": "Sunehri Masjid", "religion": "Muslim", "state": "Delhi", "city": "Delhi"},
    {"name": "Asafi Mosque", "religion": "Muslim", "state": "Telangana", "city": "Hyderabad"},
    {"name": "Nagore Dargah", "religion": "Muslim", "state": "Tamil Nadu", "city": "Nagore"},

    # SIKH (10)
    {"name": "Golden Temple", "religion": "Sikh", "state": "Punjab", "city": "Amritsar"},
    {"name": "Akal Takht", "religion": "Sikh", "state": "Punjab", "city": "Amritsar"},
    {"name": "Anandpur Sahib", "religion": "Sikh", "state": "Punjab", "city": "Anandpur Sahib"},
    {"name": "Takht Sri Patna Sahib", "religion": "Sikh", "state": "Bihar", "city": "Patna"},
    {"name": "Takht Sri Hazur Sahib", "religion": "Sikh", "state": "Maharashtra", "city": "Nanded"},
    {"name": "Hemkund Sahib", "religion": "Sikh", "state": "Uttarakhand", "city": "Chamoli"},
    {"name": "Gurudwara Bangla Sahib", "religion": "Sikh", "state": "Delhi", "city": "Delhi"},
    {"name": "Gurudwara Sis Ganj Sahib", "religion": "Sikh", "state": "Delhi", "city": "Delhi"},
    {"name": "Gurudwara Manikaran Sahib", "religion": "Sikh", "state": "Himachal Pradesh", "city": "Manikaran"},
    {"name": "Gurudwara Sri Tarn Taran Sahib", "religion": "Sikh", "state": "Punjab", "city": "Tarn Taran"},

    # CHRISTIAN (15)
    {"name": "Basilica of Bom Jesus", "religion": "Christian", "state": "Goa", "city": "Old Goa"},
    {"name": "Velankanni Church", "religion": "Christian", "state": "Tamil Nadu", "city": "Velankanni"},
    {"name": "St. Thomas Cathedral Basilica", "religion": "Christian", "state": "Kerala", "city": "Chennai"},
    {"name": "Santhome Cathedral Basilica", "religion": "Christian", "state": "Tamil Nadu", "city": "Chennai"},
    {"name": "Se Cathedral", "religion": "Christian", "state": "Goa", "city": "Old Goa"},
    {"name": "St. Francis Church", "religion": "Christian", "state": "Goa", "city": "Old Goa"},
    {"name": "Sacred Heart Cathedral", "religion": "Christian", "state": "Karnataka", "city": "New Delhi"},
    {"name": "Medak Cathedral", "religion": "Christian", "state": "Telangana", "city": "Medak"},
    {"name": "St. Paul’s Cathedral", "religion": "Christian", "state": "Kolkata", "city": "Kolkata"},
    {"name": "St. Mary’s Basilica", "religion": "Christian", "state": "Karnataka", "city": "Bangalore"},
    {"name": "Infant Jesus Shrine", "religion": "Christian", "state": "Karnataka", "city": "Bangalore"},
    {"name": "Our Lady of the Rosary Church", "religion": "Christian", "state": "Goa", "city": "Vasco da Gama"},
    {"name": "Malayattoor Church", "religion": "Christian", "state": "Kerala", "city": "Malayattoor"},
    {"name": "St. Alphonsa Shrine", "religion": "Christian", "state": "Kerala", "city": "Kochi"},
    {"name": "St. Michael’s Cathedral", "religion": "Christian", "state": "Arunachal Pradesh", "city": "Itanagar"},

    # BUDDHIST (10)
    {"name": "Mahabodhi Temple", "religion": "Buddhist", "state": "Bihar", "city": "Bodh Gaya"},
    {"name": "Sarnath", "religion": "Buddhist", "state": "Uttar Pradesh", "city": "Varanasi"},
    {"name": "Rumtek Monastery", "religion": "Buddhist", "state": "Sikkim", "city": "Gangtok"},
    {"name": "Tawang Monastery", "religion": "Buddhist", "state": "Arunachal Pradesh", "city": "Tawang"},
    {"name": "Namdroling Monastery", "religion": "Buddhist", "state": "Karnataka", "city": "Bylakuppe"},
    {"name": "Hemis Monastery", "religion": "Buddhist", "state": "Ladakh", "city": "Hemis"},
    {"name": "Thiksey Monastery", "religion": "Buddhist", "state": "Ladakh", "city": "Thiksey"},
    {"name": "Dhamek Stupa", "religion": "Buddhist", "state": "Uttar Pradesh", "city": "Sarnath"},
    {"name": "Nalanda Mahavihara", "religion": "Buddhist", "state": "Bihar", "city": "Nalanda"},
    {"name": "Ajanta Caves", "religion": "Buddhist", "state": "Maharashtra", "city": "Aurangabad"},

    # JAIN (10)
    {"name": "Palitana Temples", "religion": "Jain", "state": "Gujarat", "city": "Palitana"},
    {"name": "Shravanabelagola", "religion": "Jain", "state": "Karnataka", "city": "Shravanabelagola"},
    {"name": "Dilwara Temples", "religion": "Jain", "state": "Rajasthan", "city": "Mount Abu"},
    {"name": "Ranakpur Jain Temple", "religion": "Jain", "state": "Rajasthan", "city": "Ranakpur"},
    {"name": "Shikharji", "religion": "Jain", "state": "Jharkhand", "city": "Giridih"},
    {"name": "Girnar Temples", "religion": "Jain", "state": "Gujarat", "city": "Junagadh"},
    {"name": "Sonagiri Jain Temples", "religion": "Jain", "state": "Madhya Pradesh", "city": "Datia"},
    {"name": "Kundalpur", "religion": "Jain", "state": "Bihar", "city": "Kundalpur"},
    {"name": "Khajuraho Jain Temples", "religion": "Jain", "state": "Madhya Pradesh", "city": "Khajuraho"},
    {"name": "Moodabidri Jain Temple", "religion": "Jain", "state": "Karnataka", "city": "Moodabidri"}
]

# Add default placeholders
for lm in landmarks:
    lm["opening_hours"] = "06:00 - 20:00"
    lm["entry_fee"] = "Free"
    lm["peak_festival"] = ""
    lm["latitude"] = ""
    lm["longitude"] = ""

# Convert to DataFrame
df = pd.DataFrame(landmarks)

# Save CSV
df.to_csv("india_religious_landmarks_phase1.csv", index=False)
print("✅ CSV generated successfully: india_religious_landmarks_phase1.csv")