Hospital Management System

Team Name: Apathon
Author: Mirza Ayaan Baig
        Ashank Kotain
        Abhijay Jindal
Project Title: Hospital Management System

Description

A simple console-based hospital management system using Python and OOP.
Data is stored in .txt files using JSON format.
Supports patients, doctors, appointments, and medical records.

Concepts Used

OOP (classes, objects)
File handling
JSON data storage
Modular code
Basic CLI menus
Libraries
json
os
datetime
typing (optional)


Main Components

Models-
Classes for Patient, Doctor, Appointment, and MedicalRecord.
Each has a to_dict() method for saving data.

FileStorage-
Handles reading and writing lists of records to .txt files.

HospitalSystem-
Core logic for add/list/search/delete features, appointment handling, and medical record management.

CLI Menu-
Provides simple number-based options to navigate the system.

Example-
Adding a patient stores a record like:
{"patient_id": "P001", "name": "Ali", "age": 21}

Setup-
Install Python 3
Make sure these files exist (or they will be created automatically):
patients.txt, doctors.txt, appointments.txt, records.txt

Run the program-
python hospital_system.py


