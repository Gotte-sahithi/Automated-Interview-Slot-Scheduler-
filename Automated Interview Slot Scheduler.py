import random

# =====================================
# CO1: Problem Formulation & System Design
# Define interview slots and candidate data
# =====================================

slots = ["Monday 10:00 AM", "Monday 11:00 AM", "Monday 12:00 PM"]

candidates = [
    {"id": "C1", "name": "Charitha", "slots": [slots[0], slots[1]], "priority": "High"},
    {"id": "C2", "name": "Sahithi", "slots": [slots[1], slots[2]], "priority": "Medium"},
    {"id": "C3", "name": "Sabiya", "slots": [slots[0], slots[2]], "priority": "Low"}
]

interviewer = "Dr. Ashok"

# =====================================
# CO4: Utility-Based Decision Making
# Priority scores used for scheduling
# =====================================

utility_score = {
    "High": 100,
    "Medium": 70,
    "Low": 40
}

schedule_db = {}
busy_slots = []

print("\n===== AUTOMATED INTERVIEW SLOT SCHEDULER =====")

# =====================================
# CO4: Sort candidates based on utility
# Higher priority candidates scheduled first
# =====================================

candidates.sort(
    key=lambda x: utility_score[x["priority"]],
    reverse=True
)

for candidate in candidates:

    # =====================================
    # CO2: A* Search Slot Selection
    # Simplified A* → choose first available slot
    # =====================================
    best_slot = candidate["slots"][0]

    # =====================================
    # CO3: CSP & Conflict Management
    # Check whether slot is already occupied
    # =====================================
    if best_slot not in busy_slots:

        busy_slots.append(best_slot)

        # =====================================
        # CO5: Probabilistic Scheduling
        # Predict cancellation probability
        # =====================================
        probability = round(random.uniform(0, 1), 2)

        if probability > 0.7:
            risk = "High"
        elif probability > 0.4:
            risk = "Medium"
        else:
            risk = "Low"

        schedule_db[candidate["name"].lower()] = (
            interviewer,
            best_slot
        )

        # =====================================
        # CO6: Integration & Reporting
        # Display complete schedule details
        # =====================================
        print("\n====================================")
        print("Candidate           :", candidate["name"])
        print("Interviewer         :", interviewer)
        print("Priority            :", candidate["priority"])
        print("Utility Score       :", utility_score[candidate["priority"]])
        print("Assigned Slot       :", best_slot)
        print("Cancellation Chance :", probability)
        print("Risk Level          :", risk)
        print("====================================")

    else:
        print(f"Conflict detected for {candidate['name']}")

# =====================================
# CO6: Search Module
# Retrieve scheduled interview details
# =====================================

print("\n===== SEARCH MODULE =====")

name = input("\nEnter Candidate Name to Search: ").lower()

if name in schedule_db:
    interviewer_name, slot = schedule_db[name]

    print("\nSEARCH RESULT")
    print("Candidate  :", name.title())
    print("Interviewer:", interviewer_name)
    print("Schedule   :", slot)
else:
    print("Candidate not found.")
