import heapq
import random
import time
from dataclasses import dataclass
from typing import List, Dict, Set

# =====================================================
# CO1 : PROBLEM FORMULATION & SYSTEM DESIGN
# =====================================================

@dataclass(frozen=True)
class TimeSlot:
    day: str
    hour: str


@dataclass
class Candidate:
    id: str
    name: str
    available_slots: List[TimeSlot]
    priority: str


@dataclass
class Interviewer:
    id: str
    name: str
    available_slots: List[TimeSlot]


# =====================================================
# CO2 : A* SEARCH SLOT SELECTION
# =====================================================

class AStarScheduler:

    def select_best_slot(self, candidate_slots):

        priority_queue = []

        for index, slot in enumerate(candidate_slots):
            cost = 1
            heuristic = index + 1
            total_cost = cost + heuristic

            heapq.heappush(
                priority_queue,
                (total_cost, slot.day, slot.hour, slot)
            )

        return heapq.heappop(priority_queue)[3]


# =====================================================
# CO3 : CSP & CONFLICT MANAGEMENT
# =====================================================

class CSPScheduler:

    def __init__(self):
        self.busy_map: Dict[TimeSlot, Set[str]] = {}
        self.assignments = {}

    def is_consistent(self, interviewer_name, slot):

        if slot in self.busy_map:
            if interviewer_name in self.busy_map[slot]:
                return False

        return True

    def assign(self, candidate, interviewer_name, slot):

        if not self.is_consistent(interviewer_name, slot):
            return False

        self.assignments[candidate.id] = (
            interviewer_name,
            slot
        )

        if slot not in self.busy_map:
            self.busy_map[slot] = set()

        self.busy_map[slot].add(interviewer_name)

        return True


# =====================================================
# CO4 : UTILITY BASED DECISION MAKING
# =====================================================

def utility(priority):

    utility_table = {
        "High": 100,
        "Medium": 70,
        "Low": 40
    }

    return utility_table.get(priority, 0)


# =====================================================
# CO5 : PROBABILISTIC SCHEDULING
# =====================================================

def predict_cancellation():

    probability = round(random.uniform(0, 1), 2)

    if probability > 0.7:
        risk = "High"

    elif probability > 0.4:
        risk = "Medium"

    else:
        risk = "Low"

    return probability, risk


# =====================================================
# CO6 : INTEGRATION & PERFORMANCE ANALYSIS
# =====================================================

class AutomatedInterviewScheduler:

    def __init__(self):

        self.astar = AStarScheduler()
        self.csp = CSPScheduler()

        self.schedule_database = {}

    def schedule_candidate(self, candidate, interviewer):

        best_slot = self.astar.select_best_slot(
            candidate.available_slots
        )

        start_time = time.perf_counter()

        success = self.csp.assign(
            candidate,
            interviewer.name,
            best_slot
        )

        end_time = time.perf_counter()

        execution_time = (
            end_time - start_time
        ) * 1000

        if success:

            probability, risk = predict_cancellation()

            self.schedule_database[
                candidate.name.lower()
            ] = (
                interviewer.name,
                best_slot
            )

            print("\n====================================")
            print("Candidate           :", candidate.name)
            print("Interviewer         :", interviewer.name)
            print("Priority            :", candidate.priority)
            print("Utility Score       :", utility(candidate.priority))
            print(
                "Assigned Slot       :",
                best_slot.day,
                best_slot.hour
            )
            print(
                "Cancellation Chance :",
                probability
            )
            print(
                "Risk Level          :",
                risk
            )
            print(
                f"Execution Time      : {execution_time:.4f} ms"
            )
            print("====================================")

        else:
            print(
                f"Conflict detected for {candidate.name}"
            )

    def search_candidate(self, name):

        key = name.lower()

        if key in self.schedule_database:

            interviewer, slot = self.schedule_database[key]

            print("\nSEARCH RESULT")
            print("Candidate  :", name)
            print("Interviewer:", interviewer)
            print(
                "Schedule   :",
                slot.day,
                slot.hour
            )

        else:
            print("Candidate not found.")


# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    slot1 = TimeSlot("Monday", "10:00 AM")
    slot2 = TimeSlot("Monday", "11:00 AM")
    slot3 = TimeSlot("Monday", "12:00 PM")

    interviewer1 = Interviewer(
        "I1",
        "Dr. Ashok",
        [slot1, slot2, slot3]
    )

    candidates = [

        Candidate(
            "C1",
            "Charitha",
            [slot1, slot2],
            "High"
        ),

        Candidate(
            "C2",
            "Sahithi",
            [slot2, slot3],
            "Medium"
        ),

        Candidate(
            "C3",
            "Sabiya",
            [slot1, slot3],
            "Low"
        )
    ]

    scheduler = AutomatedInterviewScheduler()

    print(
        "\n===== AUTOMATED INTERVIEW SLOT SCHEDULER ====="
    )

    candidates.sort(
        key=lambda x: utility(x.priority),
        reverse=True
    )

    for candidate in candidates:

        scheduler.schedule_candidate(
            candidate,
            interviewer1
        )

    print("\n===== SEARCH MODULE =====")

    search_name = input(
        "\nEnter Candidate Name to Search: "
    )

    scheduler.search_candidate(search_name)
