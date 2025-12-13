from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List

app = FastAPI(title="Career Bridge Pro")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Domain-based skills
DOMAIN_SKILLS: Dict[str, Dict[str, List[str]]] = {
    "Web Development": {
        "must": ["HTML", "CSS", "JavaScript"],
        "core": ["React", "Node.js", "Projects"],
        "advanced": ["Next.js", "Performance Optimization"]
    },
    "Data Science": {
        "must": ["Python", "Statistics", "Pandas"],
        "core": ["Machine Learning", "Data Visualization", "Projects"],
        "advanced": ["Deep Learning", "Big Data Tools"]
    },
    "AI/ML": {
        "must": ["Python", "Linear Algebra", "Probability"],
        "core": ["Machine Learning Algorithms", "Data Preprocessing", "Projects"],
        "advanced": ["Deep Learning", "NLP", "Computer Vision"]
    },
    "Embedded Systems": {
        "must": ["C/C++", "Microcontrollers", "Digital Logic"],
        "core": ["Arduino", "RTOS", "Sensors/Actuators"],
        "advanced": ["IoT Projects", "PCB Design"]
    }
}

# Calculate match score
def calculate_score(required: Dict[str, List[str]], known: List[str]) -> int:
    total_skills = sum(len(skills) for skills in required.values())
    matched_skills = sum(
        1 for skills in required.values() for skill in skills if skill in known
    )
    return int((matched_skills / total_skills) * 100)

# API endpoint
@app.post("/analyze")
def analyze(data: Dict):
    """
    Input JSON: {"domain": "Web Development", "skills": ["HTML","CSS"]}
    Output: score, gaps, roadmap, verdict
    """
    domain: str = data.get("domain")
    known: List[str] = data.get("skills", [])

    if domain not in DOMAIN_SKILLS:
        return {"error": f"Domain '{domain}' not found."}

    required = DOMAIN_SKILLS[domain]

    score = calculate_score(required, known)

    # Skill gaps per level
    gaps = {level: [skill for skill in skills if skill not in known]
            for level, skills in required.items()}

    # Build roadmap dynamically
    roadmap: List[str] = []
    for level in ["must", "core", "advanced"]:
        for skill in gaps[level]:
            roadmap.append(f"Week plan → Learn {skill}")

    verdict = "Job Ready" if score > 70 else "Skill Gap Exists"

    return {
        "score": score,
        "gaps": gaps,
        "roadmap": roadmap,
        "verdict": verdict
    }
