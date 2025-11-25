Hospital Management System

Team Name: Apathon

Author: Mirza Ayaan Baig
        Ashank Kotian
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
Models

Classes for Patient, Doctor, Appointment, and MedicalRecord.
Each has to_dict() for saving data.

FileStorage

Handles reading/writing lists of records to .txt files.

HospitalSystem

Core logic: add/list/search/delete for all modules + appointment and record management.

CLI Menu

Runs the system with simple numbered options.

Example

Adding a patient stores a record like:

{"patient_id": "P001", "name": "Ali", "age": 21}

Setup

Install Python 3

Ensure files exist (or will be auto-created):
patients.txt, doctors.txt, appointments.txt, records.txt

Run:

python hospital_system.py


If you want an ultra-minimal one-paragraph README, I can generate that too.

