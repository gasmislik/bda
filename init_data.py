import pandas as pd
import os

os.makedirs("data", exist_ok=True)

# ===============================
# Formations
# ===============================
formations = pd.DataFrame([
    {"id": 1, "nom": "Software Engineering", "dept_id": 1},
    {"id": 2, "nom": "Computer Science", "dept_id": 1},
])

formations.to_csv("data/formations.csv", index=False)

# ===============================
# Groupes
# ===============================
groupes = pd.DataFrame([
    {"id": 1, "nom": "SE-1", "formation_id": 1},
    {"id": 2, "nom": "SE-2", "formation_id": 1},
    {"id": 3, "nom": "CS-1", "formation_id": 2},
])

groupes.to_csv("data/groupes.csv", index=False)

# ===============================
# Modules
# ===============================
modules = pd.DataFrame([
    {"id": 1, "nom": "Algorithms", "formation_id": 1},
    {"id": 2, "nom": "Databases", "formation_id": 1},
    {"id": 3, "nom": "Operating Systems", "formation_id": 2},
])

modules.to_csv("data/modules.csv", index=False)

# ===============================
# Professors
# ===============================
profs = pd.DataFrame([
    {"id": 1, "nom": "Prof. Smith"},
    {"id": 2, "nom": "Prof. Johnson"},
    {"id": 3, "nom": "Prof. Lee"},
])

profs.to_csv("data/professeurs.csv", index=False)

# ===============================
# Rooms
# ===============================
salles = pd.DataFrame([
    {"id": 1, "nom": "Room A", "capacite": 40},
    {"id": 2, "nom": "Room B", "capacite": 60},
    {"id": 3, "nom": "Amphi 1", "capacite": 120},
])

salles.to_csv("data/salles.csv", index=False)

# ===============================
# Time slots
# ===============================
creneaux = pd.DataFrame([
    {"id": 1, "heure": "08:00-09:30"},
    {"id": 2, "heure": "10:00-11:30"},
    {"id": 3, "heure": "13:00-14:30"},
    {"id": 4, "heure": "15:00-16:30"},
])

creneaux.to_csv("data/creneaux.csv", index=False)

# ===============================
# Student groups
# ===============================
etudiant_groupes = pd.DataFrame(
    [{"etudiant_id": i, "groupe_id": 1} for i in range(1, 41)] +
    [{"etudiant_id": i, "groupe_id": 2} for i in range(41, 71)] +
    [{"etudiant_id": i, "groupe_id": 3} for i in range(71, 101)]
)

etudiant_groupes.to_csv("data/etudiant_groupes.csv", index=False)

# ===============================
# Empty examens
# ===============================
examens = pd.DataFrame(columns=[
    "groupe", "module", "prof", "salle",
    "date_exam", "formation", "departement"
])

examens.to_csv("data/examens.csv", index=False)

print("✔ All CSV files created successfully.")
