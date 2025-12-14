from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DATA = {
    "web": {
        "have": ["HTML", "CSS"],
        "missing": ["JavaScript", "React", "APIs"],
        "roadmap": [
            "Master JavaScript fundamentals",
            "Learn React basics",
            "Build 3 real projects",
            "Practice APIs & backend integration"
        ]
    },
    "ai": {
        "have": ["Python"],
        "missing": ["ML", "Deep Learning", "TensorFlow"],
        "roadmap": [
            "Learn ML basics",
            "Understand Deep Learning",
            "Practice with TensorFlow",
            "Build ML projects"
        ]
    },
    "iot": {
        "have": ["C", "Sensors"],
        "missing": ["Microcontrollers", "Cloud IoT"],
        "roadmap": [
            "Learn Arduino / ESP32",
            "Work with sensors",
            "Connect IoT to cloud",
            "Build smart system"
        ]
    }
}

@app.get("/analyze")
def analyze(domain: str):
    skills = DATA[domain]
    score = int(len(skills["have"]) / (len(skills["have"]) + len(skills["missing"])) * 100)

    return {
        "score": score,
        "verdict": "Good Progress" if score >= 50 else "Needs Improvement",
        "skills": skills,
        "roadmap": skills["roadmap"]
    }
