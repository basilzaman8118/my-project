from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import re
from difflib import get_close_matches

app = FastAPI()

# --- CORS Setup for Angular ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Configuration ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "hospital_db"
}

def query_db(query, params=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# --- Helper: Fuzzy Matching ---
def fuzzy_match(word, choices):
    matches = get_close_matches(word.lower(), [c.lower() for c in choices], n=1, cutoff=0.6)
    return matches[0] if matches else None


@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "").lower()

    try:
        # --- Synonym Mapping ---
        synonyms = {
            "heart": "cardiology",
            "cardio": "cardiology",
            "brain": "neurology",
            "nerve": "neurology",
            "bone": "orthopedic",
            "child": "pediatrics",
            "kids": "pediatrics",
            "medicine": "pharmacy",
            "drug": "pharmacy",
            "tablet": "pharmacy"
        }

        for key, val in synonyms.items():
            if key in question:
                question = question.replace(key, val)

        # --- Logic 1: Doctors ---
        if "doctor" in question or "specialist" in question:
            specs = [d["specialization"] for d in query_db("SELECT DISTINCT specialization FROM doctors;")]
            match = None
            for spec in specs:
                matched = fuzzy_match(question, [spec])
                if matched:
                    match = spec
                    break

            if match:
                doctors = query_db("SELECT name FROM doctors WHERE specialization LIKE %s;", (f"%{match}%",))
                if doctors:
                    # ✅ Remove duplicates
                    unique_names = sorted(set([d["name"] for d in doctors]))
                    result = ", ".join(unique_names)
                    return {"answer": f"Doctors specializing in {match}: {result}"}
                else:
                    return {"answer": f"No doctors found in {match}."}
            else:
                all_doctors = query_db("SELECT name, specialization FROM doctors;")
                seen = set()
                result = []
                for d in all_doctors:
                    key = (d["name"], d["specialization"])
                    if key not in seen:
                        seen.add(key)
                        result.append(f"{d['name']} ({d['specialization']})")
                return {"answer": f"Available doctors: {', '.join(result)}"}

        # --- Logic 2: Department Locations ---
        elif "department" in question or "where" in question:
            depts = query_db("SELECT name, location FROM departments;")
            names = [d["name"] for d in depts]
            matched = fuzzy_match(question, names)
            if matched:
                dept = query_db("SELECT name, location FROM departments WHERE name LIKE %s;", (f"%{matched}%",))
                if dept:
                    d = dept[0]
                    return {"answer": f"The {d['name']} department is located at {d['location']}."}
            return {"answer": "I couldn’t find that department. Please check the name."}

        # --- Logic 3: Medicine Stock ---
        elif "medicine" in question or "available" in question or "stock" in question:
            meds = query_db("SELECT name, quantity FROM medicines WHERE quantity > 0;")
            if meds:
                # ✅ Remove duplicates and sort
                seen = {}
                for m in meds:
                    seen[m["name"]] = m["quantity"]
                med_list = ", ".join([f"{name} ({qty} left)" for name, qty in sorted(seen.items())])
                return {"answer": f"Available medicines: {med_list}"}
            return {"answer": "No medicines currently available."}

        # --- Logic 4: Patient Info ---
        elif "patient" in question:
            patients = query_db("SELECT name, age FROM patients LIMIT 5;")
            if patients:
                # ✅ Remove duplicates
                unique_patients = {(p["name"], p["age"]) for p in patients}
                result = ", ".join([f"{name} (age {age})" for name, age in sorted(unique_patients)])
                return {"answer": f"Here are some patients: {result}"}
            return {"answer": "No patient data available."}

        # --- Logic 5: Appointments ---
        elif "appointment" in question:
            appointments = query_db("""
                SELECT p.name AS patient, d.name AS doctor, a.appointment_date, a.status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                JOIN doctors d ON a.doctor_id = d.id
                ORDER BY a.appointment_date DESC LIMIT 5;
            """)
            if appointments:
                # ✅ Remove duplicates
                seen = set()
                lines = []
                for a in appointments:
                    key = (a["patient"], a["doctor"], str(a["appointment_date"]), a["status"])
                    if key not in seen:
                        seen.add(key)
                        lines.append(f"{a['patient']} with {a['doctor']} on {a['appointment_date']} ({a['status']})")
                return {"answer": "Recent appointments:\n" + "\n".join(lines)}
            return {"answer": "No appointments found."}

        # --- Logic 6: FAQ or fallback ---
        else:
            faq = query_db("SELECT answer FROM faq WHERE question LIKE %s;", (f"%{question}%",))
            if faq:
                return {"answer": faq[0]["answer"]}
            return {"answer": "I'm not sure about that. Could you please rephrase?"}

    except Exception as e:
        return {"answer": f"⚠️ Database error: {str(e)}"}
