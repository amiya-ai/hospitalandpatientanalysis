"""
Hospital & Patient Analysis - Dataset Generator
Generates a realistic, statistically coherent healthcare dataset.
"""

import os
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_healthcare_data(num_records=1500, output_path="data/healthcare_dataset.csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(42)
    np.random.seed(42)

    first_names = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
        "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
        "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa",
        "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
        "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
        "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
        "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
        "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Frank", "Debra",
        "Alexander", "Rachel", "Raymond", "Catherine", "Patrick", "Carolyn", "Jack", "Janet",
        "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
        "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
        "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
        "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
        "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
        "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey"
    ]

    hospitals = [
        "Memorial General Hospital",
        "St. Jude Health Center",
        "Metropolitan Medical Center",
        "City Care Hospital",
        "Horizon Valley Medical Institute",
        "St. Luke Regional Hospital"
    ]

    doctors = [
        "Dr. Michael Harris (Cardiology)",
        "Dr. Sarah Jenkins (Endocrinology)",
        "Dr. Robert Chen (Pulmonology)",
        "Dr. Emily Watson (Oncology)",
        "Dr. David Kim (Orthopedics)",
        "Dr. Lisa Patel (Internal Medicine)",
        "Dr. Anthony Ross (Emergency Medicine)",
        "Dr. Amanda Brooks (Neurology)",
        "Dr. Christopher Lee (General Surgery)",
        "Dr. Jessica Taylor (Infectious Disease)"
    ]

    medical_conditions = [
        "Hypertension", "Diabetes", "Asthma", "Cardiovascular Disease", 
        "Arthritis", "Cancer", "Pneumonia", "Chronic Kidney Disease"
    ]

    insurance_providers = ["Medicare", "Blue Cross", "Aetna", "Cigna", "UnitedHealthcare"]
    blood_types = ["O+", "A+", "B+", "AB+", "O-", "A-", "B-", "AB-"]
    admission_types = ["Emergency", "Elective", "Urgent"]
    test_results = ["Normal", "Abnormal", "Inconclusive"]

    condition_medications = {
        "Hypertension": ["Lisinopril", "Amlodipine", "Losartan", "Hydrochlorothiazide"],
        "Diabetes": ["Metformin", "Insulin Glargine", "Glipizide", "Januvia"],
        "Asthma": ["Albuterol", "Fluticasone", "Montelukast", "Budesonide"],
        "Cardiovascular Disease": ["Atorvastatin", "Clopidogrel", "Metoprolol", "Aspirin"],
        "Arthritis": ["Ibuprofen", "Methotrexate", "Celecoxib", "Naproxen"],
        "Cancer": ["Tamoxifen", "Cisplatin", "Paclitaxel", "Doxorubicin"],
        "Pneumonia": ["Azithromycin", "Amoxicillin", "Ceftriaxone", "Levofloxacin"],
        "Chronic Kidney Disease": ["Erythropoietin", "Furosemide", "Calcium Acetate", "Calcitriol"]
    }

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range_days = (end_date - start_date).days

    records = []

    for i in range(1, num_records + 1):
        patient_id = f"PAT-{10000 + i}"
        first = random.choice(first_names)
        last = random.choice(last_names)
        name = f"{first} {last}"
        gender = random.choice(["Male", "Female"])
        
        # Age distribution: older population has higher prevalence
        age = int(np.random.normal(54, 18))
        age = max(18, min(92, age))

        blood_type = random.choice(blood_types)
        
        # Condition weighting based on age
        if age > 60:
            cond_weights = [0.22, 0.20, 0.08, 0.20, 0.12, 0.08, 0.05, 0.05]
        elif age > 40:
            cond_weights = [0.20, 0.18, 0.15, 0.12, 0.12, 0.08, 0.08, 0.07]
        else:
            cond_weights = [0.12, 0.10, 0.25, 0.08, 0.10, 0.05, 0.20, 0.10]
            
        condition = np.random.choice(medical_conditions, p=cond_weights)
        doctor = random.choice(doctors)
        hospital = random.choice(hospitals)
        insurance = random.choice(insurance_providers)
        admission_type = random.choice(admission_types)
        
        # Test results correlated with condition severity
        if condition in ["Cancer", "Cardiovascular Disease", "Chronic Kidney Disease"]:
            test_res = np.random.choice(test_results, p=[0.20, 0.65, 0.15])
        else:
            test_res = np.random.choice(test_results, p=[0.50, 0.35, 0.15])

        medication = random.choice(condition_medications[condition])

        # Date of Admission
        random_days = random.randint(0, date_range_days)
        admission_date = start_date + timedelta(days=random_days)

        # Length of stay depends on condition and admission type
        base_stay = {
            "Cancer": 12, "Cardiovascular Disease": 9, "Chronic Kidney Disease": 8,
            "Pneumonia": 7, "Diabetes": 5, "Hypertension": 4, "Arthritis": 3, "Asthma": 3
        }[condition]

        if admission_type == "Emergency":
            base_stay += random.randint(2, 5)
        elif admission_type == "Urgent":
            base_stay += random.randint(1, 3)

        los = max(1, int(np.random.normal(base_stay, 2.5)))
        discharge_date = admission_date + timedelta(days=los)

        # Billing amount correlated with stay, admission type, condition
        base_bill = 2000 + (los * random.randint(900, 1600))
        if condition in ["Cancer", "Cardiovascular Disease"]:
            base_bill += random.randint(8000, 22000)
        elif admission_type == "Emergency":
            base_bill += random.randint(3000, 7000)
        
        billing_amount = round(base_bill + random.uniform(50, 950), 2)

        # Room assignment
        room_number = random.randint(101, 599)

        # Readmission probability
        readmit_prob = 0.12
        if age > 65:
            readmit_prob += 0.08
        if test_res == "Abnormal":
            readmit_prob += 0.08
        if condition in ["Cardiovascular Disease", "Chronic Kidney Disease"]:
            readmit_prob += 0.07

        readmission = "Yes" if random.random() < min(0.65, readmit_prob) else "No"

        # Treatment outcome
        if readmission == "Yes" and test_res == "Abnormal":
            outcome = np.random.choice(["Discharged with Home Care", "Under Intensive Observation", "Transferred"], p=[0.45, 0.40, 0.15])
        else:
            outcome = np.random.choice(["Fully Recovered", "Discharged with Home Care", "Stable on Medication"], p=[0.50, 0.35, 0.15])

        records.append({
            "Patient_ID": patient_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Blood_Type": blood_type,
            "Medical_Condition": condition,
            "Date_of_Admission": admission_date.strftime("%Y-%m-%d"),
            "Discharge_Date": discharge_date.strftime("%Y-%m-%d"),
            "Length_of_Stay": los,
            "Doctor": doctor,
            "Hospital": hospital,
            "Insurance_Provider": insurance,
            "Billing_Amount": billing_amount,
            "Room_Number": room_number,
            "Admission_Type": admission_type,
            "Medication": medication,
            "Test_Results": test_res,
            "Readmission": readmission,
            "Treatment_Outcome": outcome
        })

    df = pd.DataFrame(records)
    df.sort_values(by="Date_of_Admission", inplace=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created with {len(df)} records at: {output_path}")
    return df

if __name__ == "__main__":
    generate_healthcare_data()
