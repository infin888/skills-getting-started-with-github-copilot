"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice skills, teamwork, and compete in matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Learn fundamentals, run drills, and play scrimmages",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["taylor@mergington.edu"]
    },

    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Thursdays, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": ["mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and rehearsals for school performances",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["liam@mergington.edu"]
    },

    "Debate Team": {
        "description": "Develop research, argumentation, and public speaking skills",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["ava@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for competitions",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 24,
        "participants": ["noah@mergington.edu"]
    },
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html", status_code=302)


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    normalized_email = email.strip().lower()
    if any(p.strip().lower() == normalized_email for p in activity["participants"]):
        raise HTTPException(status_code=409, detail="Student already signed up")

    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
