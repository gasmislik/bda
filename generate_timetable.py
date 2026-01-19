import pandas as pd
from datetime import date, timedelta
from collections import defaultdict
from random import shuffle
import time


modules = pd.read_csv("data/modules.csv").to_dict("records")
groupes = pd.read_csv("data/groupes.csv").to_dict("records")
formations = pd.read_csv("data/formations.csv").to_dict("records")
profs = pd.read_csv("data/professeurs.csv").to_dict("records")
salles = pd.read_csv("data/salles.csv").to_dict("records")
creneaux = pd.read_csv("data/creneaux.csv").to_dict("records")[:4]
etudiant_groupes = pd.read_csv("data/etudiant_groupes.csv").to_dict("records")

START_DATE = date(2025, 1, 10)
NB_DAYS = 20
DUREE = 90

group_size = defaultdict(int)
for eg in etudiant_groupes:
    group_size[eg["groupe_id"]] += 1

student_day = {}
prof_day = defaultdict(int)
prof_total = defaultdict(int)
room_usage = set()

generated_examens = []

def available_profs(exam_date):
    profs_ok = [p for p in profs if prof_day[(p["id"], exam_date)] < 3]
    return sorted(profs_ok, key=lambda p: prof_total[p["id"]])

def available_rooms(group_id, exam_date, creneau_id):
    size = group_size[group_id]
    result = []

    for s in salles:
        key = (s["id"], exam_date, creneau_id)
        if key not in room_usage and size <= s["capacite"]:
            result.append(s)

    return result

def generate_schedule():
    for g in groupes:
        group_modules = [
            m for m in modules
            if m["formation_id"] == g["formation_id"]
        ]

        for m in group_modules:
            placed = False

            for d in range(NB_DAYS):
                exam_date = START_DATE + timedelta(days=d)

                if student_day.get((g["id"], exam_date)):
                    continue

                shuffled_creneaux = creneaux.copy()
                shuffle(shuffled_creneaux)

                for c in shuffled_creneaux:
                    rooms = available_rooms(g["id"], exam_date, c["id"])
                    profs_ok = available_profs(exam_date)

                    if not rooms or not profs_ok:
                        continue

                    prof = profs_ok[0]
                    salle = rooms[0]

                    generated_examens.append({
                        "groupe": g["nom"],
                        "module": m["nom"],
                        "prof": prof["nom"],
                        "salle": salle["nom"],
                        "date_exam": exam_date.strftime("%Y-%m-%d"),
                        "formation": next(
                            f["nom"] for f in formations
                            if f["id"] == g["formation_id"]
                        ),
                        "departement": "Unknown"
                    })

                    student_day[(g["id"], exam_date)] = 1
                    prof_day[(prof["id"], exam_date)] += 1
                    prof_total[prof["id"]] += 1
                    room_usage.add((salle["id"], exam_date, c["id"]))

                    placed = True
                    break

                if placed:
                    break

if __name__ == "__main__":
    start = time.time()
    generate_schedule()

    pd.DataFrame(generated_examens).to_csv(
        "data/examens.csv", index=False
    )

    print("Timetable generated.")
    print("Execution time:", round(time.time() - start, 2), "sec")
