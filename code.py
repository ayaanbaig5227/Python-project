#!/usr/bin/env python3
"""
Hospital Management System (OOP, file-backed using .txt files storing JSON)
Save this file as hospital_system.py and run: python hospital_system.py
"""

import json
import os
import datetime
from typing import List, Optional, Dict, Any

# ---------- Models ----------
class Patient:
    def __init__(self, patient_id: str, name: str, age: int, gender: str, phone: str, notes: str = ""):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.notes = notes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "notes": self.notes
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Patient":
        return Patient(d["patient_id"], d["name"], d["age"], d["gender"], d["phone"], d.get("notes", ""))


class Doctor:
    def __init__(self, doctor_id: str, name: str, speciality: str, phone: str):
        self.doctor_id = doctor_id
        self.name = name
        self.speciality = speciality
        self.phone = phone

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "speciality": self.speciality,
            "phone": self.phone
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Doctor":
        return Doctor(d["doctor_id"], d["name"], d["speciality"], d["phone"])


class Appointment:
    def __init__(self, appointment_id: str, patient_id: str, doctor_id: str, dt: str, reason: str = ""):
        # dt should be ISO formatted string 'YYYY-MM-DD HH:MM'
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.dt = dt
        self.reason = reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "appointment_id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "dt": self.dt,
            "reason": self.reason
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Appointment":
        return Appointment(d["appointment_id"], d["patient_id"], d["doctor_id"], d["dt"], d.get("reason", ""))


# ---------- Storage ----------
class Storage:
    """
    Manages saving and loading lists of dicts to/from text files (JSON inside).
    """
    def __init__(self, folder: str = "."):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self.folder, filename)

    def save_list(self, filename: str, items: List[Dict[str, Any]]):
        path = self._path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

    def load_list(self, filename: str) -> List[Dict[str, Any]]:
        path = self._path(filename)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []


# ---------- Hospital System ----------
class HospitalSystem:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.patients: Dict[str, Patient] = {}
        self.doctors: Dict[str, Doctor] = {}
        self.appointments: Dict[str, Appointment] = {}
        self._load_all()

    # --- Persistence ---
    def _load_all(self):
        for p in self.storage.load_list("patients.txt"):
            pat = Patient.from_dict(p)
            self.patients[pat.patient_id] = pat
        for d in self.storage.load_list("doctors.txt"):
            doc = Doctor.from_dict(d)
            self.doctors[doc.doctor_id] = doc
        for a in self.storage.load_list("appointments.txt"):
            appt = Appointment.from_dict(a)
            self.appointments[appt.appointment_id] = appt

    def _save_all(self):
        self.storage.save_list("patients.txt", [p.to_dict() for p in self.patients.values()])
        self.storage.save_list("doctors.txt", [d.to_dict() for d in self.doctors.values()])
        self.storage.save_list("appointments.txt", [a.to_dict() for a in self.appointments.values()])

    # --- Utilities ---
    @staticmethod
    def _next_id(prefix: str, existing: Dict[str, Any]) -> str:
        # generate sequential ID like P1, P2, D1, A1...
        max_idx = 0
        for k in existing.keys():
            if k.startswith(prefix):
                try:
                    idx = int(k[len(prefix):])
                    if idx > max_idx:
                        max_idx = idx
                except ValueError:
                    continue
        return f"{prefix}{max_idx + 1}"

    # --- Patient CRUD ---
    def add_patient(self, name: str, age: int, gender: str, phone: str, notes: str = "") -> Patient:
        pid = self._next_id("P", self.patients)
        patient = Patient(pid, name, age, gender, phone, notes)
        self.patients[pid] = patient
        self._save_all()
        return patient

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        return self.patients.get(patient_id)

    def find_patients_by_name(self, name: str) -> List[Patient]:
        name_lower = name.lower()
        return [p for p in self.patients.values() if name_lower in p.name.lower()]

    def delete_patient(self, patient_id: str) -> bool:
        if patient_id in self.patients:
            # also remove appointments of this patient
            self.appointments = {aid: a for aid, a in self.appointments.items() if a.patient_id != patient_id}
            del self.patients[patient_id]
            self._save_all()
            return True
        return False

    # --- Doctor CRUD ---
    def add_doctor(self, name: str, speciality: str, phone: str) -> Doctor:
        did = self._next_id("D", self.doctors)
        doctor = Doctor(did, name, speciality, phone)
        self.doctors[did] = doctor
        self._save_all()
        return doctor

    def get_doctor(self, doctor_id: str) -> Optional[Doctor]:
        return self.doctors.get(doctor_id)

    def find_doctors_by_name(self, name: str) -> List[Doctor]:
        name_lower = name.lower()
        return [d for d in self.doctors.values() if name_lower in d.name.lower()]

    def delete_doctor(self, doctor_id: str) -> bool:
        if doctor_id in self.doctors:
            # also remove appointments with this doctor
            self.appointments = {aid: a for aid, a in self.appointments.items() if a.doctor_id != doctor_id}
            del self.doctors[doctor_id]
            self._save_all()
            return True
        return False

    # --- Appointments ---
    def schedule_appointment(self, patient_id: str, doctor_id: str, dt_str: str, reason: str = "") -> Appointment:
        # dt_str: 'YYYY-MM-DD HH:MM'
        # basic validation
        if patient_id not in self.patients:
            raise ValueError("Patient not found")
        if doctor_id not in self.doctors:
            raise ValueError("Doctor not found")
        try:
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Datetime format should be YYYY-MM-DD HH:MM")

        # check for overlapping appointment for same doctor at exact same time
        for a in self.appointments.values():
            if a.doctor_id == doctor_id and a.dt == dt_str:
                raise ValueError("Doctor already has an appointment at that time")

        aid = self._next_id("A", self.appointments)
        appt = Appointment(aid, patient_id, doctor_id, dt_str, reason)
        self.appointments[aid] = appt
        self._save_all()
        return appt

    def cancel_appointment(self, appointment_id: str) -> bool:
        if appointment_id in self.appointments:
            del self.appointments[appointment_id]
            self._save_all()
            return True
        return False

    def list_appointments_for_doctor(self, doctor_id: str) -> List[Appointment]:
        return sorted([a for a in self.appointments.values() if a.doctor_id == doctor_id],
                      key=lambda x: x.dt)

    def list_appointments_for_patient(self, patient_id: str) -> List[Appointment]:
        return sorted([a for a in self.appointments.values() if a.patient_id == patient_id],
                      key=lambda x: x.dt)

    # --- Helpers to display ---
    def display_patients(self):
        if not self.patients:
            print("No patients found.")
            return
        print("Patients:")
        for p in self.patients.values():
            print(f"  {p.patient_id}: {p.name}, age {p.age}, {p.gender}, phone {p.phone}")

    def display_doctors(self):
        if not self.doctors:
            print("No doctors found.")
            return
        print("Doctors:")
        for d in self.doctors.values():
            print(f"  {d.doctor_id}: Dr. {d.name} ({d.speciality}), phone {d.phone}")

    def display_appointments(self):
        if not self.appointments:
            print("No appointments.")
            return
        print("Appointments:")
        for a in sorted(self.appointments.values(), key=lambda x: x.dt):
            p = self.patients.get(a.patient_id)
            d = self.doctors.get(a.doctor_id)
            print(f"  {a.appointment_id}: {a.dt} - Patient: {p.name if p else a.patient_id} | Doctor: {d.name if d else a.doctor_id} | Reason: {a.reason}")


# ---------- CLI ----------
def input_int(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        if s.isdigit():
            return int(s)
        print("Please enter a valid integer.")

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")

def main_menu():
    print("\n=== Hospital Management System ===")
    print("1. Patients")
    print("2. Doctors")
    print("3. Appointments")
    print("4. Show all")
    print("0. Exit")

def patients_menu():
    print("\n--- Patients Menu ---")
    print("1. Add patient")
    print("2. View all patients")
    print("3. Search patients by name")
    print("4. Delete patient")
    print("0. Back")

def doctors_menu():
    print("\n--- Doctors Menu ---")
    print("1. Add doctor")
    print("2. View all doctors")
    print("3. Search doctors by name")
    print("4. Delete doctor")
    print("0. Back")

def appointments_menu():
    print("\n--- Appointments Menu ---")
    print("1. Schedule appointment")
    print("2. View all appointments")
    print("3. View appointments for patient")
    print("4. View appointments for doctor")
    print("5. Cancel appointment")
    print("0. Back")

def run_cli():
    storage = Storage(folder="hospital_data")
    hs = HospitalSystem(storage)

    while True:
        main_menu()
        choice = input_nonempty("Choose an option: ")
        if choice == "1":
            while True:
                patients_menu()
                c = input_nonempty("Choose: ")
                if c == "1":
                    name = input_nonempty("Name: ")
                    age = input_int("Age: ")
                    gender = input_nonempty("Gender: ")
                    phone = input_nonempty("Phone: ")
                    notes = input("Notes (optional): ").strip()
                    p = hs.add_patient(name, age, gender, phone, notes)
                    print(f"Added patient {p.patient_id} - {p.name}")
                elif c == "2":
                    hs.display_patients()
                elif c == "3":
                    q = input_nonempty("Search name: ")
                    res = hs.find_patients_by_name(q)
                    if not res:
                        print("No patients found.")
                    else:
                        for p in res:
                            print(f"  {p.patient_id}: {p.name}, age {p.age}, phone {p.phone}")
                elif c == "4":
                    pid = input_nonempty("Patient ID to delete: ")
                    ok = hs.delete_patient(pid)
                    print("Deleted." if ok else "Patient not found.")
                elif c == "0":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "2":
            while True:
                doctors_menu()
                c = input_nonempty("Choose: ")
                if c == "1":
                    name = input_nonempty("Name: ")
                    speciality = input_nonempty("Speciality: ")
                    phone = input_nonempty("Phone: ")
                    d = hs.add_doctor(name, speciality, phone)
                    print(f"Added doctor {d.doctor_id} - Dr. {d.name}")
                elif c == "2":
                    hs.display_doctors()
                elif c == "3":
                    q = input_nonempty("Search name: ")
                    res = hs.find_doctors_by_name(q)
                    if not res:
                        print("No doctors found.")
                    else:
                        for d in res:
                            print(f"  {d.doctor_id}: Dr. {d.name}, {d.speciality}, phone {d.phone}")
                elif c == "4":
                    did = input_nonempty("Doctor ID to delete: ")
                    ok = hs.delete_doctor(did)
                    print("Deleted." if ok else "Doctor not found.")
                elif c == "0":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "3":
            while True:
                appointments_menu()
                c = input_nonempty("Choose: ")
                if c == "1":
                    pid = input_nonempty("Patient ID: ")
                    did = input_nonempty("Doctor ID: ")
                    dt = input_nonempty("Datetime (YYYY-MM-DD HH:MM): ")
                    reason = input("Reason (optional): ").strip()
                    try:
                        appt = hs.schedule_appointment(pid, did, dt, reason)
                        print(f"Appointment scheduled: {appt.appointment_id} at {appt.dt}")
                    except Exception as e:
                        print(f"Error: {e}")
                elif c == "2":
                    hs.display_appointments()
                elif c == "3":
                    pid = input_nonempty("Patient ID: ")
                    arr = hs.list_appointments_for_patient(pid)
                    if not arr:
                        print("No appointments for patient.")
                    else:
                        for a in arr:
                            d = hs.doctors.get(a.doctor_id)
                            print(f"  {a.appointment_id}: {a.dt} with Dr. {d.name if d else a.doctor_id} | Reason: {a.reason}")
                elif c == "4":
                    did = input_nonempty("Doctor ID: ")
                    arr = hs.list_appointments_for_doctor(did)
                    if not arr:
                        print("No appointments for doctor.")
                    else:
                        for a in arr:
                            p = hs.patients.get(a.patient_id)
                            print(f"  {a.appointment_id}: {a.dt} - Patient: {p.name if p else a.patient_id} | Reason: {a.reason}")
                elif c == "5":
                    aid = input_nonempty("Appointment ID to cancel: ")
                    ok = hs.cancel_appointment(aid)
                    print("Cancelled." if ok else "Appointment not found.")
                elif c == "0":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "4":
            print("\n--- All Data ---")
            hs.display_patients()
            print()
            hs.display_doctors()
            print()
            hs.display_appointments()
        elif choice == "0":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    run_cli()
