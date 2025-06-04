import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Symptom number to description map
symptom_map = {
    "10": "Feeling nervous, anxious, or on edge",
    "11": "Not being able to stop or control worrying",
    "12": "Worrying too much about different things",
    "13": "Trouble relaxing",
    "14": "Being so restless that it is hard to sit still",
    "15": "Becoming easily annoyed or irritable",
    "16": "Feeling afraid, as if something awful might happen"
}

# Theme keywords map
theme_keywords = {
    "Academic issue": ["exam", "assignment", "marks", "study", "project", "test", "college", "class", "professor"],
    "Family issue": ["parents", "mother", "father", "home", "family", "uncle", "aunt", "siblings"],
    "Lifestyle Factor": ["sleep", "food", "exercise", "routine", "health", "diet", "habits"],
    "Social Factor": ["friends", "roommate", "party", "outing", "cricket", "social", "conversation", "talk"],
    "Psychological Factor": ["anxiety", "fear", "worry", "panic", "overthink", "guilt", "burnout", "mood"],
    "Medical Co-morbidity": ["illness", "pain", "headache", "fever", "fatigue", "sick", "medicine"]
}

def load_symptoms_data(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                data.append((row[0].strip(), row[1].strip()))
    return data


def detect_symptom(user_input, data):
    for text, symptom_num in data:
        if text.strip() in user_input.strip():
            symptom_nums = symptom_num.split(',')
            symptoms = [symptom_map.get(num.strip(), f"Unknown ({num.strip()})") for num in symptom_nums]
            return symptoms
    return []


def save_frequency_to_csv(frequency, filename="symptom_frequency_log.csv"):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for symptom, count in frequency.items():
            writer.writerow([symptom, count])


def calculate_intensity_score(frequency):
    total_score = 0
    for count in frequency.values():
        if 0 <= count <= 2:
            total_score += 0
        elif 3 <= count <= 6:
            total_score += 1
        elif 7 <= count <= 10:
            total_score += 2
        elif 11 <= count <= 15:
            total_score += 3

    if 0 <= total_score <= 4:
        return "Minimal anxiety"
    elif 5 <= total_score <= 9:
        return "Mild anxiety"
    elif 10 <= total_score <= 14:
        return "Moderate anxiety"
    elif 15 <= total_score <= 21:
        return "Severe anxiety"
    else:
        return "Invalid Score"


def detect_theme_from_texts(texts):
    theme_counts = defaultdict(int)
    for text in texts:
        lower_text = text.lower()
        for theme, keywords in theme_keywords.items():
            for keyword in keywords:
                if keyword in lower_text:
                    theme_counts[theme] += 1
    if theme_counts:
        return max(theme_counts, key=theme_counts.get)
    else:
        return "No clear theme detected"


def load_doctors_by_city(filename, city_name):
    doctors = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['City'].strip().lower() == city_name.strip().lower():
                doctors.append(row)
    return doctors


# ✅ NEW: Plot symptom frequency across 15 days (for report window)
def generate_symptom_graph(daywise_dict):
    plt.figure(figsize=(12, 6))
    days = [f"Day {i}" for i in range(1, 16)]

    for symptom, symptom_days in daywise_dict.items():
        values = [1 if f"Day {i}" in symptom_days else 0 for i in range(1, 16)]
        plt.plot(days, values, marker='o', label=symptom)

    plt.title("Symptom Presence Over 15 Days")
    plt.xlabel("Days")
    plt.ylabel("Symptoms")
    plt.yticks([])  # Optional: hide numeric y-axis
    plt.legend(loc='upper right', fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
