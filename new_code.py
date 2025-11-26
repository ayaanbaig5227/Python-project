import json, os
from datetime import datetime

# data folder
DATA_DIR = "hospital_db"

# helper to check folder
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

# --- Classes ---

class Patient:
    def __init__(self, id, name, age, gender, ph, notes=""):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = ph
        self.notes = notes

    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "notes": self.notes
        }

class Doctor:
    def __init__(self, id, name, spec, ph):
        self.id = id
        self.name = name
        self.spec = spec
        self.phone = ph
    
    def get_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "spec": self.spec,
            "phone": self.phone
        }

class Appt:
    def __init__(self, id, pid, did, time, reason):
        self.id = id
        self.pid = pid
        self.did = did
        self.time = time
        self.reason = reason

    def get_dict(self):
        return {
            "id": self.id,
            "pid": self.pid,
            "did": self.did,
            "time": self.time,
            "reason": self.reason
        }

# Main Logic
class ManagementSystem:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appts = []
        self.load() 

    def load(self):
        # Loading patients
        p_file = DATA_DIR + "/patients.json"
        if os.path.exists(p_file):
            try:
                with open(p_file, "r") as f:
                    data = json.load(f)
                    for d in data:
                        obj = Patient(d['id'], d['name'], d['age'], d['gender'], d['phone'], d.get('notes', ''))
                        self.patients.append(obj)
            except:
                print("Error loading patients")

        # Loading doctors
        d_file = DATA_DIR + "/doctors.json"
        if os.path.exists(d_file):
            try:
                with open(d_file, "r") as f:
                    data = json.load(f)
                    for item in data:
                        doc = Doctor(item['id'], item['name'], item['spec'], item['phone'])
                        self.doctors.append(doc)
            except:
                pass 

        # Loading appointments
        a_file = DATA_DIR + "/appts.json"
        if os.path.exists(a_file):
            try:
                with open(a_file, "r") as f:
                    raw = json.load(f)
                    for r in raw:
                        self.appts.append(Appt(r['id'], r['pid'], r['did'], r['time'], r['reason']))
            except:
                pass

    def save(self):
        # save patients
        temp_p = []
        for p in self.patients:
            temp_p.append(p.get_dict())
        
        with open(DATA_DIR + "/patients.json", "w") as f:
            json.dump(temp_p, f, indent=4)

        # save doctors
        temp_d = []
        for d in self.doctors:
            temp_d.append(d.get_dict())
            
        with open(DATA_DIR + "/doctors.json", "w") as f:
            json.dump(temp_d, f, indent=4)

        # save appointments
        temp_a = [x.get_dict() for x in self.appts]
        with open(DATA_DIR + "/appts.json", "w") as f:
            json.dump(temp_a, f, indent=4)

    # --- UPDATED ID GENERATION ---
    def get_new_id(self, type):
        # Determine the list and the prefix based on type
        data_list = []
        prefix = ""
        
        if type == "P":
            data_list = self.patients
            prefix = "P"
        elif type == "D":
            data_list = self.doctors
            prefix = "D"
        elif type == "A":
            data_list = self.appts
            prefix = "A"
        else:
            return "UNKNOWN"

        # Find the highest existing number in the IDs
        max_id = 0
        for item in data_list:
            try:
                # id is like "A1", "A12". We slice [1:] to get the number.
                num_part = int(item.id[1:])
                if num_part > max_id:
                    max_id = num_part
            except:
                pass # skip if ID format is weird
        
        # Return next number
        return prefix + str(max_id + 1)

    def add_pat(self):
        print("--- New Patient ---")
        n = input("Name: ")
        a = input("Age: ")
        if not a.isdigit():#checking if input in int
            print("Invalid age")
            return
        g = input("Gender: ")
        ph = input("Phone: ")
        note = input("Notes: ")
        
        pid = self.get_new_id("P")
        new_p = Patient(pid, n, int(a), g, ph, note)
        self.patients.append(new_p)
        self.save()
        print("Patient Saved: " + pid)

    def add_doc(self):
        print("--- New Doctor ---")
        n = input("Name: ")
        s = input("Speciality: ")
        ph = input("Phone: ")
        
        did = self.get_new_id("D")
        self.doctors.append(Doctor(did, n, s, ph))
        self.save()
        print("Doctor Saved: " + did)

    def schedule(self):
        print("--- Book Appointment ---")
        pid = input("Patient ID: ")
        found_p = False
        for p in self.patients:
            if p.id == pid:
                found_p = True
                break
        
        if not found_p:
            print("Patient not found!")
            return

        did = input("Doctor ID: ")
        found_d = False
        for d in self.doctors:
            if d.id == did:
                found_d = True
                break
        
        if not found_d:
            print("Doctor not found!")
            return

        t = input("Time (YYYY-MM-DD HH:MM): ")
        if len(t) < 10:
            print("Invalid date format")
            return
        
        for a in self.appts:
            if a.did == did and a.time == t:
                print("Doctor is busy then.")
                return

        reason = input("Reason: ")
        aid = self.get_new_id("A")
        self.appts.append(Appt(aid, pid, did, t, reason))
        self.save()
        print("Booked.")

    def cancel_appt(self):
        print("--- Cancel Appointment ---")
        aid = input("Appointment ID (e.g. A1): ")
        
        found = False
        for a in self.appts:
            if a.id == aid:
                self.appts.remove(a)
                found = True
                break
        
        if found:
            self.save()
            print("Appointment Cancelled.")
        else:
            print("Appointment ID not found.")

    def show_all(self):
        print("\n--- DATA DUMP ---")
        print(f"Patients: {len(self.patients)}")
        for p in self.patients:
            print(f"{p.id}: {p.name}")
        
        print(f"\nDoctors: {len(self.doctors)}")
        for d in self.doctors:
            print(f"{d.id}: {d.name} ({d.spec})")
            
        print(f"\nAppointments: {len(self.appts)}")
        for a in self.appts:
            print(f"[{a.id}] {a.time}: {a.pid} with {a.did}")

    def run(self):
        while True:
            print("\n1. Add Patient")
            print("2. Add Doctor")
            print("3. Book Appt")
            print("4. Cancel Appt")
            print("5. Show Data")
            print("6. Exit")
            
            sel = input("Select: ")
            
            if sel == "1":
                self.add_pat()
            elif sel == "2":
                self.add_doc()
            elif sel == "3":
                self.schedule()
            elif sel == "4":
                self.cancel_appt()
            elif sel == "5":
                self.show_all()
            elif sel == "6":
                break
            else:
                print("Wrong input")

# start
if __name__ == "__main__":
    sys = ManagementSystem()
    sys.run()
