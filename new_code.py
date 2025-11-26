import json
import os

# 1. Simple Classes without complex static methods
class Patient:
    def __init__(self, id, name, age, gender, phone, notes=""):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.notes = notes

class Doctor:
    def __init__(self, id, name, speciality, phone):
        self.id = id
        self.name = name
        self.speciality = speciality
        self.phone = phone

class Appointment:
    def __init__(self, id, patient_id, doctor_id, date_time, reason=""):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_time = date_time
        self.reason = reason

# 2. Main System Class handles logic AND file saving directly
class HospitalManager:
    def __init__(self):
        # We store data in lists instead of dictionaries (easier to loop through for students)
        self.patients = []
        self.doctors = []
        self.appointments = []
        
        # Hardcoded folder name
        self.data_folder = "hospital_data"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
            
        self.load_data()

    # --- File Handling (Directly inside the class) ---
    def load_data(self):
        # Load Patients
        if os.path.exists(f"{self.data_folder}/patients.json"):
            with open(f"{self.data_folder}/patients.json", "r") as f:
                data = json.load(f)
                for p in data:
                    new_patient = Patient(p['id'], p['name'], p['age'], p['gender'], p['phone'], p['notes'])
                    self.patients.append(new_patient)

        # Load Doctors
        if os.path.exists(f"{self.data_folder}/doctors.json"):
            with open(f"{self.data_folder}/doctors.json", "r") as f:
                data = json.load(f)
                for d in data:
                    new_doc = Doctor(d['id'], d['name'], d['speciality'], d['phone'])
                    self.doctors.append(new_doc)

        # Load Appointments
        if os.path.exists(f"{self.data_folder}/appointments.json"):
            with open(f"{self.data_folder}/appointments.json", "r") as f:
                data = json.load(f)
                for a in data:
                    new_appt = Appointment(a['id'], a['patient_id'], a['doctor_id'], a['date_time'], a['reason'])
                    self.appointments.append(new_appt)

    def save_data(self):
        # Convert objects to dictionaries manually
        p_data = [vars(p) for p in self.patients]
        d_data = [vars(d) for d in self.doctors]
        a_data = [vars(a) for a in self.appointments]

        with open(f"{self.data_folder}/patients.json", "w") as f:
            json.dump(p_data, f, indent=4)
        with open(f"{self.data_folder}/doctors.json", "w") as f:
            json.dump(d_data, f, indent=4)
        with open(f"{self.data_folder}/appointments.json", "w") as f:
            json.dump(a_data, f, indent=4)

    # --- Helpers ---
    def generate_id(self, prefix, current_list):
        # A simple way to generate IDs based on list length
        return f"{prefix}{len(current_list) + 1}"

    # --- Features ---
    def add_patient(self):
        print("\n--- Add Patient ---")
        name = input("Enter Name: ")
        age = input("Enter Age: ")
        gender = input("Enter Gender: ")
        phone = input("Enter Phone: ")
        notes = input("Notes (optional): ")
        
        pid = self.generate_id("P", self.patients)
        new_patient = Patient(pid, name, age, gender, phone, notes)
        self.patients.append(new_patient)
        self.save_data()
        print(f"Patient added successfully! ID: {pid}")

    def view_patients(self):
        print("\n--- All Patients ---")
        if not self.patients:
            print("No patients found.")
        else:
            for p in self.patients:
                print(f"ID: {p.id} | Name: {p.name} | Age: {p.age} | Phone: {p.phone}")

    def search_patient(self):
        name = input("Enter name to search: ").lower()
        found = False
        for p in self.patients:
            if name in p.name.lower():
                print(f"Found: ID: {p.id} | Name: {p.name}")
                found = True
        if not found:
            print("No matching patients found.")

    def delete_patient(self):
        pid = input("Enter Patient ID to delete: ")
        # Using a standard loop to find and remove
        for i, p in enumerate(self.patients):
            if p.id == pid:
                del self.patients[i]
                self.save_data()
                print("Patient deleted.")
                return
        print("Patient ID not found.")

    def add_doctor(self):
        print("\n--- Add Doctor ---")
        name = input("Enter Name: ")
        spec = input("Speciality: ")
        phone = input("Phone: ")
        
        did = self.generate_id("D", self.doctors)
        doctor = Doctor(did, name, spec, phone)
        self.doctors.append(doctor)
        self.save_data()
        print(f"Doctor added! ID: {did}")

    def view_doctors(self):
        print("\n--- All Doctors ---")
        for d in self.doctors:
            print(f"ID: {d.id} | Dr. {d.name} ({d.speciality})")

    def schedule_appointment(self):
        pid = input("Enter Patient ID: ")
        did = input("Enter Doctor ID: ")
        
        # Validation using flags
        p_exists = False
        for p in self.patients:
            if p.id == pid:
                p_exists = True
        
        d_exists = False
        for d in self.doctors:
            if d.id == did:
                d_exists = True
                
        if not p_exists:
            print("Error: Patient ID invalid.")
            return
        if not d_exists:
            print("Error: Doctor ID invalid.")
            return

        # Simple string for date, no datetime complexity
        date_time = input("Enter Date/Time (e.g., 2023-10-20 10:00 AM): ")
        reason = input("Reason: ")

        aid = self.generate_id("A", self.appointments)
        appt = Appointment(aid, pid, did, date_time, reason)
        self.appointments.append(appt)
        self.save_data()
        print(f"Appointment Scheduled! ID: {aid}")

    def view_appointments(self):
        print("\n--- Appointments ---")
        if not self.appointments:
            print("No appointments.")
        for a in self.appointments:
            # Simple lookup without complex helper methods
            p_name = "Unknown"
            d_name = "Unknown"
            
            for p in self.patients:
                if p.id == a.patient_id:
                    p_name = p.name
            for d in self.doctors:
                if d.id == a.doctor_id:
                    d_name = d.name
            
            print(f"[{a.id}] {a.date_time} | Patient: {p_name} | Dr. {d_name} | Reason: {a.reason}")


# Main Menu Loop
def main():
    system = HospitalManager()
    
    while True:
        print("\n=== Hospital System ===")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Add Doctor")
        print("5. View Doctors")
        print("6. Schedule Appointment")
        print("7. View Appointments")
        print("8. Delete Patient")
        print("0. Exit")
        
        choice = input("Select option: ")

        if choice == '1':
            system.add_patient()
        elif choice == '2':
            system.view_patients()
        elif choice == '3':
            system.search_patient()
        elif choice == '4':
            system.add_doctor()
        elif choice == '5':
            system.view_doctors()
        elif choice == '6':
            system.schedule_appointment()
        elif choice == '7':
            system.view_appointments()
        elif choice == '8':
            system.delete_patient()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
