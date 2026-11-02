"""
Helper to export JSON data for the standalone HTML dashboard.
"""
import json
import pandas as pd
from analysis_engine import load_data, calculate_kpis, get_disease_distribution, get_hospital_metrics, get_insurance_breakdown

def export_json():
    df = load_data("data/healthcare_dataset.csv")
    kpis = calculate_kpis(df)
    diseases = get_disease_distribution(df).to_dict(orient="records")
    hospitals = get_hospital_metrics(df).to_dict(orient="records")
    insurance = get_insurance_breakdown(df).to_dict(orient="records")
    
    # Sample 300 patients for instant table browsing
    sample_records = df.head(300).copy()
    sample_records["Date_of_Admission"] = sample_records["Date_of_Admission"].astype(str)
    sample_records["Discharge_Date"] = sample_records["Discharge_Date"].astype(str)
    patients = sample_records.to_dict(orient="records")

    payload = {
        "kpis": kpis,
        "diseases": diseases,
        "hospitals": hospitals,
        "insurance": insurance,
        "patients": patients,
        "total_count": len(df)
    }

    with open("data/dashboard_data.json", "w") as f:
        json.dump(payload, f, indent=2)
    print("Exported dashboard_data.json successfully!")

if __name__ == "__main__":
    export_json()
