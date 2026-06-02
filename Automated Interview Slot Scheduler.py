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

    def __str__(self):
        return f"{self.day} at {self.hour}"


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


# =====================================================
# CO2 : A* SEARCH SLOT SELECTION
# =====================================================

class AStarScheduler:

    def select_best_slot(self, candidate_slots: List[TimeSlot]):
        if not candidate_slots:
            return None

        priority_queue = []

        for index, slot in enumerate(candidate_slots):
            cost = 1
            heuristic = index + 1
            total_cost = cost + heuristic

            heapq.heappush(
                priority_queue,
                (total_cost, index, slot)
            )

        return heapq.heappop(priority_queue)[2]


# =====================================================
# CO3 : CSP SCHEDULING
# =====================================================

class CSPScheduler:

    def __init__(self):
        # Maps an interviewer's slot key to a set of assigned candidates
        self.busy_map: Dict[str, Set[str]] = {}
        self.assignments = {}

    def is_consistent(self, interviewer_name, slot):
        key = (
            f"{interviewer_name}_"
            f"{slot.day.lower()}_"
            f"{slot.hour.lower()}"
        )
        return key not in self.busy_map

    def assign(self, candidate, interviewer_name, slot):
        if not self.is_consistent(interviewer_name, slot):
            return False

        key = (
            f"{interviewer_name}_"
            f"{slot.day.lower()}_"
            f"{slot.hour.lower()}"
        )

        # Fixes the overwriting bug by cleanly initializing/adding to the reservation
        if key not in self.busy_map:
            self.busy_map[key] = set()
        self.busy_map[key].add(candidate.name)

        self.assignments[candidate.id] = (
            interviewer_name,
            slot
        )
        return True


# =====================================================
# CO4 : UTILITY FUNCTION
# =====================================================

def calculate_utility(priority):
    table = {
        "High": 100,
        "Medium": 70,
        "Low": 40
    }
    return table.get(priority, 50)


# =====================================================
# CO5 : PROBABILISTIC INFERENCE
# =====================================================

def infer_cancellation_risk():
    probability = round(
        random.uniform(0.10, 0.95),
        2
    )

    if probability > 0.70:
        risk = "High Risk"
    elif probability > 0.40:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return probability, risk


# =====================================================
# CO6 : INTEGRATED AI AGENT
# =====================================================

class AutomatedInterviewScheduler:

    def __init__(self, fallback_hours):
        self.astar = AStarScheduler()
        self.csp = CSPScheduler()
        self.fallback_hours = fallback_hours
        self.schedule_database = {}

    def assign_available_interviewer(self, interviewers, slot):
        for interviewer in interviewers:
            if self.csp.is_consistent(interviewer.name, slot):
                return interviewer
        return None

    def schedule_candidate(self, candidate, interviewers):
        print(f"\n--- Scheduling {candidate.name} ---")

        slots_to_try = list(candidate.available_slots)

        while slots_to_try:
            best_slot = self.astar.select_best_slot(slots_to_try)
            
            # Prevent infinite loops by removing the checked slot
            if best_slot in slots_to_try:
                slots_to_try.remove(best_slot)

            if best_slot.day.lower() in ["saturday", "sunday"]:
                print("Weekend selected. Moved to Monday.")
                best_slot = TimeSlot("Monday", best_slot.hour)

            # Look for an interviewer available at the requested time
            interviewer = self.assign_available_interviewer(interviewers, best_slot)

            # -----------------------------------------------------------------
            # RESCHEDULE TRIGGER: Triggered when slot/interviewer combination fails
            # -----------------------------------------------------------------
            if interviewer is None:
                print(f"\n[CONFLICT DETECTED] Slot ({best_slot.day} at {best_slot.hour}) is completely booked.")
                print("Initiating automatic fallback rescheduling...")

                found = False
                for hour in self.fallback_hours:
                    alternate_slot = TimeSlot(best_slot.day, hour)
                    interviewer = self.assign_available_interviewer(interviewers, alternate_slot)

                    if interviewer:
                        best_slot = alternate_slot
                        found = True
                        print(f"-> Reschedule successful! Moved to alternate time: {hour}")
                        break

                if not found:
                    print(f"\n[RESCHEDULE FAILED] No fallbacks or alternative interviewers found for {candidate.name}.")
                    return False

            # Assign and commit the successful slot
            start = time.perf_counter()
            success = self.csp.assign(candidate, interviewer.name, best_slot)
            end = time.perf_counter()

            execution_time = (end - start) * 1000

            if success:
                self.schedule_database[candidate.name.lower()] = (interviewer.name, best_slot)
                probability, risk = infer_cancellation_risk()

                print("\n========================")
                print("Candidate :", candidate.name)
                print("Interviewer :", interviewer.name)
                print("Slot :", best_slot.day, "at", best_slot.hour)
                print("Utility :", calculate_utility(candidate.priority))
                print("Cancellation Risk :", probability, risk)
                print("Execution Time :", round(execution_time, 5), "ms")
                print("========================")
                return True

        return False

    def search_candidate(self, name):
        key = name.lower()
        if key in self.schedule_database:
            interviewer, slot = self.schedule_database[key]
            print("\n===== RECORD FOUND =====")
            print("Candidate :", name)
            print("Interviewer :", interviewer)
            print("Schedule :", slot.day, "at", slot.hour)
        else:
            print("Record not found.")


# =====================================================
# MAIN PROGRAM
# =====================================================

if __name__ == "__main__":

    system_hours = [
        "10:00 AM",
        "11:00 AM",
        "12:00 PM",
        "02:00 PM",
        "03:00 PM"
    ]

    interviewers = [
        Interviewer("I1", "Dr. Ashok"),
        Interviewer("I2", "Dr. Srinivasan"),
        Interviewer("I3", "Dr. Radhika"),
        Interviewer("I4", "Prof. Anand"),
        Interviewer("I5", "Dr. K. Satya Prasad")
    ]

    scheduler = AutomatedInterviewScheduler(fallback_hours=system_hours)

    while True:
        print("\n===== INTERVIEW REGISTRATION =====")
        name = input("Enter Candidate Name (or exit): ").strip()

        if name.lower() == "exit":
            break

        priority = input("Enter Priority (High/Medium/Low): ").strip().capitalize()
        if priority not in ["High", "Medium", "Low"]:
            priority = "Medium"

        day = input("Enter Preferred Day: ").strip().capitalize()
        hour = input("Enter Preferred Time: ").strip().upper()

        candidate = Candidate(
            id=f"C_{random.randint(100,999)}",
            name=name,
            available_slots=[TimeSlot(day, hour)],
            priority=priority
        )

        scheduler.schedule_candidate(candidate, interviewers)

    print("\n===== SEARCH RECORD =====")
    search_name = input("Enter Candidate Name: ")
    scheduler.search_candidate(search_name)
